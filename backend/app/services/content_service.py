import google.generativeai as genai
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
import re
from slugify import slugify

from app.core.config import settings
from app.models.content import Content, ContentVersion, ContentAnalytics, ContentTemplate
from app.models.game import Game
from app.models.team import Team
from app.models.prediction import Prediction
from app.models.user import User

logger = logging.getLogger(__name__)

class ContentService:
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.model_version = "1.0.0"
        
        # Default content templates
        self.default_templates = {
            "game_analysis": {
                "name": "Game Analysis Template",
                "description": "Template for analyzing upcoming AFL games",
                "content_type": "analysis",
                "prompt_template": """
                Analyze the upcoming AFL game between {home_team} and {away_team} for Round {round_number} of the {season} season.
                
                Game Details:
                - Venue: {venue}
                - Date: {game_date}
                - Home Team: {home_team}
                - Away Team: {away_team}
                
                Historical Context:
                {historical_data}
                
                Recent Form:
                {recent_form}
                
                Please provide:
                1. A witty and engaging analysis of both teams' current form
                2. Key factors that could influence the outcome
                3. Historical head-to-head insights
                4. Betting considerations with humor
                5. A prediction with confidence level
                
                Style: Smart, witty, and entertaining for AFL betting enthusiasts. Include some humor and personality.
                """,
                "content_structure": {
                    "sections": ["introduction", "team_analysis", "key_factors", "historical_insights", "betting_analysis", "prediction"],
                    "required_fields": ["title", "summary", "content_body"],
                    "optional_fields": ["excerpt", "meta_description"]
                }
            },
            "team_preview": {
                "name": "Team Preview Template",
                "description": "Template for team season previews and analysis",
                "content_type": "preview",
                "prompt_template": """
                Create a comprehensive and entertaining preview for {team_name} ahead of the {season} AFL season.
                
                Team Information:
                - Team: {team_name}
                - Home Ground: {home_ground}
                - Coach: {coach}
                - Last Season: {last_season_performance}
                
                Key Players:
                {key_players}
                
                Season Outlook:
                {season_outlook}
                
                Please provide:
                1. An engaging introduction about the team's character and history
                2. Analysis of key players and their impact
                3. Team strengths and weaknesses with humor
                4. Season predictions and expectations
                5. Betting opportunities and considerations
                
                Style: Engaging, informative, and entertaining with witty commentary.
                """,
                "content_structure": {
                    "sections": ["introduction", "key_players", "strengths_weaknesses", "season_outlook", "betting_insights"],
                    "required_fields": ["title", "summary", "content_body"],
                    "optional_fields": ["excerpt", "meta_description"]
                }
            },
            "brownlow_analysis": {
                "name": "Brownlow Medal Analysis Template",
                "description": "Template for Brownlow Medal predictions and analysis",
                "content_type": "brownlow",
                "prompt_template": """
                Create an entertaining analysis of the Brownlow Medal race for the {season} AFL season.
                
                Season Context:
                - Season: {season}
                - Current Round: {current_round}
                - Leading Contenders: {leading_contenders}
                
                Historical Data:
                {historical_brownlow_data}
                
                Current Standings:
                {current_standings}
                
                Please provide:
                1. An engaging overview of the Brownlow Medal and its significance
                2. Analysis of leading contenders with personality
                3. Dark horse candidates and their chances
                4. Historical patterns and insights
                5. Betting opportunities and value picks
                
                Style: Sophisticated yet entertaining, with witty commentary on the race.
                """,
                "content_structure": {
                    "sections": ["introduction", "contenders_analysis", "dark_horses", "historical_insights", "betting_opportunities"],
                    "required_fields": ["title", "summary", "content_body"],
                    "optional_fields": ["excerpt", "meta_description"]
                }
            }
        }
    
    def generate_content(self, db: Session, template_name: str, context: Dict[str, Any], 
                        user_id: Optional[int] = None) -> Optional[Content]:
        """Generate content using a specific template and context."""
        try:
            # Get or create template
            template = self._get_or_create_template(db, template_name)
            if not template:
                logger.error(f"Template {template_name} not found")
                return None
            
            # Prepare prompt with context
            prompt = template.get_prompt_with_context(context)
            
            # Generate content using Gemini
            response = self.model.generate_content(prompt)
            generated_text = response.text
            
            # Parse and structure the content
            structured_content = self._parse_generated_content(generated_text, template)
            
            # Create content record
            content = Content(
                title=structured_content.get("title", f"Generated {template.content_type}"),
                slug=self._generate_slug(structured_content.get("title", f"generated-{template.content_type}")),
                content_type=template.content_type,
                summary=structured_content.get("summary", ""),
                content_body=structured_content.get("content_body", generated_text),
                excerpt=structured_content.get("excerpt", ""),
                ai_model=self.model_version,
                ai_prompt=prompt,
                ai_context=json.dumps(context),
                generation_parameters={
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "template": template_name
                },
                status="draft",
                tags=structured_content.get("tags", []),
                categories=structured_content.get("categories", []),
                created_by=user_id,
                updated_by=user_id
            )
            
            # Add relationships if context provides them
            if "game_id" in context:
                content.related_game_id = context["game_id"]
            if "team_id" in context:
                content.related_team_id = context["team_id"]
            if "prediction_id" in context:
                content.related_prediction_id = context["prediction_id"]
            
            # Save to database
            db.add(content)
            db.commit()
            db.refresh(content)
            
            # Update template usage
            template.increment_usage()
            db.commit()
            
            logger.info(f"Generated content {content.id} using template {template_name}")
            return content
            
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            db.rollback()
            return None
    
    def generate_game_analysis(self, db: Session, game_id: int, user_id: Optional[int] = None) -> Optional[Content]:
        """Generate analysis for a specific game."""
        try:
            game = db.query(Game).filter(Game.id == game_id).first()
            if not game:
                logger.error(f"Game {game_id} not found")
                return None
            
            # Get historical data
            historical_data = self._get_game_historical_data(db, game)
            recent_form = self._get_team_recent_form(db, game.home_team_id, game.away_team_id)
            
            context = {
                "home_team": game.home_team.name,
                "away_team": game.away_team.name,
                "round_number": game.round_number,
                "season": game.season,
                "venue": game.venue,
                "game_date": game.game_date.strftime("%B %d, %Y"),
                "historical_data": historical_data,
                "recent_form": recent_form,
                "game_id": game_id
            }
            
            return self.generate_content(db, "game_analysis", context, user_id)
            
        except Exception as e:
            logger.error(f"Error generating game analysis: {e}")
            return None
    
    def generate_team_preview(self, db: Session, team_id: int, season: int, user_id: Optional[int] = None) -> Optional[Content]:
        """Generate team preview for a specific season."""
        try:
            team = db.query(Team).filter(Team.id == team_id).first()
            if not team:
                logger.error(f"Team {team_id} not found")
                return None
            
            # Get team data
            team_data = self._get_team_data(db, team_id, season)
            
            context = {
                "team_name": team.name,
                "home_ground": team.home_ground,
                "season": season,
                "last_season_performance": team_data.get("last_season", "N/A"),
                "key_players": team_data.get("key_players", "To be determined"),
                "season_outlook": team_data.get("outlook", "Promising season ahead"),
                "team_id": team_id
            }
            
            return self.generate_content(db, "team_preview", context, user_id)
            
        except Exception as e:
            logger.error(f"Error generating team preview: {e}")
            return None
    
    def get_published_content(self, db: Session, content_type: Optional[str] = None, 
                            limit: int = 10, offset: int = 0) -> List[Content]:
        """Get published content with optional filtering."""
        query = db.query(Content).filter(Content.status == "published")
        
        if content_type:
            query = query.filter(Content.content_type == content_type)
        
        return query.order_by(desc(Content.published_at)).offset(offset).limit(limit).all()
    
    def get_featured_content(self, db: Session, limit: int = 5) -> List[Content]:
        """Get featured content."""
        return db.query(Content).filter(
            and_(Content.status == "published", Content.is_featured == True)
        ).order_by(desc(Content.published_at)).limit(limit).all()
    
    def update_content(self, db: Session, content_id: int, updates: Dict[str, Any], 
                      user_id: Optional[int] = None) -> Optional[Content]:
        """Update content and create version history."""
        try:
            content = db.query(Content).filter(Content.id == content_id).first()
            if not content:
                return None
            
            # Create version before updating
            version = ContentVersion(
                content_id=content_id,
                version_number=content.version + 1,
                title=content.title,
                content_body=content.content_body,
                summary=content.summary,
                excerpt=content.excerpt,
                change_reason=updates.get("change_reason", "manual_edit"),
                ai_model=content.ai_model,
                ai_prompt=content.ai_prompt,
                generation_parameters=content.generation_parameters,
                created_by=user_id
            )
            db.add(version)
            
            # Update content
            for key, value in updates.items():
                if hasattr(content, key) and key not in ["id", "created_at", "created_by"]:
                    setattr(content, key, value)
            
            content.version += 1
            content.updated_by = user_id
            content.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(content)
            
            return content
            
        except Exception as e:
            logger.error(f"Error updating content: {e}")
            db.rollback()
            return None
    
    def publish_content(self, db: Session, content_id: int, user_id: Optional[int] = None) -> bool:
        """Publish content."""
        try:
            content = db.query(Content).filter(Content.id == content_id).first()
            if not content:
                return False
            
            content.publish()
            content.updated_by = user_id
            content.updated_at = datetime.utcnow()
            
            db.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error publishing content: {e}")
            db.rollback()
            return False
    
    def track_content_view(self, db: Session, content_id: int) -> bool:
        """Track content view and update analytics."""
        try:
            content = db.query(Content).filter(Content.id == content_id).first()
            if not content:
                return False
            
            # Increment view count
            content.increment_view()
            
            # Update daily analytics
            today = datetime.utcnow().date()
            analytics = db.query(ContentAnalytics).filter(
                and_(
                    ContentAnalytics.content_id == content_id,
                    ContentAnalytics.date >= today,
                    ContentAnalytics.period_type == "daily"
                )
            ).first()
            
            if analytics:
                analytics.views += 1
            else:
                analytics = ContentAnalytics(
                    content_id=content_id,
                    date=today,
                    period_type="daily",
                    views=1
                )
                db.add(analytics)
            
            db.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error tracking content view: {e}")
            db.rollback()
            return False
    
    def _get_or_create_template(self, db: Session, template_name: str) -> Optional[ContentTemplate]:
        """Get or create a content template."""
        template = db.query(ContentTemplate).filter(ContentTemplate.name == template_name).first()
        
        if not template and template_name in self.default_templates:
            template_data = self.default_templates[template_name]
            template = ContentTemplate(
                name=template_data["name"],
                description=template_data["description"],
                content_type=template_data["content_type"],
                prompt_template=template_data["prompt_template"],
                content_structure=template_data["content_structure"],
                created_by=1  # System user
            )
            db.add(template)
            db.commit()
            db.refresh(template)
        
        return template
    
    def _parse_generated_content(self, text: str, template: ContentTemplate) -> Dict[str, Any]:
        """Parse generated content into structured format."""
        # This is a simplified parser - in production, you'd want more sophisticated parsing
        lines = text.split('\n')
        structured = {
            "title": "",
            "summary": "",
            "content_body": text,
            "excerpt": "",
            "tags": [],
            "categories": []
        }
        
        # Try to extract title from first line
        if lines and lines[0].strip():
            first_line = lines[0].strip()
            if len(first_line) < 100 and not first_line.startswith('#'):
                structured["title"] = first_line
                structured["content_body"] = '\n'.join(lines[1:])
        
        # Generate excerpt from first paragraph
        paragraphs = text.split('\n\n')
        if paragraphs:
            first_para = paragraphs[0].strip()
            if len(first_para) > 50:
                structured["excerpt"] = first_para[:200] + "..." if len(first_para) > 200 else first_para
        
        # Generate summary from content
        if len(text) > 100:
            structured["summary"] = text[:300] + "..." if len(text) > 300 else text
        
        # Add default tags and categories based on template
        structured["tags"] = ["AFL", "betting", "analysis"]
        structured["categories"] = [template.content_type]
        
        return structured
    
    def _generate_slug(self, title: str) -> str:
        """Generate URL slug from title."""
        return slugify(title, max_length=50)
    
    def _get_game_historical_data(self, db: Session, game: Game) -> str:
        """Get historical data for a game."""
        # Get recent games between these teams
        recent_games = db.query(Game).filter(
            and_(
                or_(
                    and_(Game.home_team_id == game.home_team_id, Game.away_team_id == game.away_team_id),
                    and_(Game.home_team_id == game.away_team_id, Game.away_team_id == game.home_team_id)
                ),
                Game.is_finished == True
            )
        ).order_by(desc(Game.game_date)).limit(5).all()
        
        if not recent_games:
            return "No recent head-to-head history available."
        
        history_text = f"Recent meetings between {game.home_team.name} and {game.away_team.name}:\n"
        for g in recent_games:
            if g.home_score and g.away_score:
                history_text += f"- {g.game_date.strftime('%Y')}: {g.home_team.name} {g.home_score} def {g.away_team.name} {g.away_score}\n"
        
        return history_text
    
    def _get_team_recent_form(self, db: Session, home_team_id: int, away_team_id: int) -> str:
        """Get recent form for both teams."""
        form_text = "Recent form:\n"
        
        for team_id in [home_team_id, away_team_id]:
            team = db.query(Team).filter(Team.id == team_id).first()
            if team:
                recent_games = db.query(Game).filter(
                    and_(
                        or_(Game.home_team_id == team_id, Game.away_team_id == team_id),
                        Game.is_finished == True
                    )
                ).order_by(desc(Game.game_date)).limit(3).all()
                
                form_text += f"\n{team.name}: "
                if recent_games:
                    for g in recent_games:
                        if g.home_team_id == team_id:
                            result = "W" if g.home_score > g.away_score else "L"
                        else:
                            result = "W" if g.away_score > g.home_score else "L"
                        form_text += f"{result} "
                else:
                    form_text += "No recent games"
        
        return form_text
    
    def _get_team_data(self, db: Session, team_id: int, season: int) -> Dict[str, Any]:
        """Get team data for preview generation."""
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            return {}
        
        # Get last season performance
        last_season_games = db.query(Game).filter(
            and_(
                or_(Game.home_team_id == team_id, Game.away_team_id == team_id),
                Game.season == season - 1,
                Game.is_finished == True
            )
        ).all()
        
        wins = 0
        for g in last_season_games:
            if g.home_team_id == team_id and g.home_score > g.away_score:
                wins += 1
            elif g.away_team_id == team_id and g.away_score > g.home_score:
                wins += 1
        
        return {
            "last_season": f"{wins} wins from {len(last_season_games)} games",
            "key_players": "Star players to watch this season",
            "outlook": "Promising season ahead with strong squad"
        } 