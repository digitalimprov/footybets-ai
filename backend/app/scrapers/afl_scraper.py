import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.game import Game
from app.models.team import Team
import logging

logger = logging.getLogger(__name__)

class AFLScraper:
    def __init__(self):
        self.base_url = settings.afl_tables_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': settings.user_agent
        })
        
    def get_season_data(self, season: int) -> List[Dict]:
        """Scrape all games for a specific season"""
        games = []
        
        try:
            # Get the season page
            season_url = f"{self.base_url}/seas/{season}.html"
            response = self.session.get(season_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all round tables
            round_tables = soup.find_all('table', class_='sortable')
            
            for round_num, table in enumerate(round_tables, 1):
                round_games = self._parse_round_table(table, season, round_num)
                games.extend(round_games)
                
                # Respectful delay
                time.sleep(settings.scraping_delay)
                
        except Exception as e:
            logger.error(f"Error scraping season {season}: {e}")
            
        return games
    
    def _parse_round_table(self, table, season: int, round_num: int) -> List[Dict]:
        """Parse a round table to extract game data"""
        games = []
        
        try:
            rows = table.find_all('tr')[1:]  # Skip header row
            
            for game_num, row in enumerate(rows, 1):
                cells = row.find_all('td')
                
                if len(cells) >= 8:  # Ensure we have enough cells
                    game_data = self._extract_game_data(cells, season, round_num, game_num)
                    if game_data:
                        games.append(game_data)
                        
        except Exception as e:
            logger.error(f"Error parsing round {round_num}: {e}")
            
        return games
    
    def _extract_game_data(self, cells, season: int, round_num: int, game_num: int) -> Optional[Dict]:
        """Extract game data from table cells"""
        try:
            # Extract team names and scores
            home_team = cells[0].get_text(strip=True)
            away_team = cells[1].get_text(strip=True)
            
            # Extract scores
            home_score_text = cells[2].get_text(strip=True)
            away_score_text = cells[3].get_text(strip=True)
            
            # Parse scores (format: "goals.behinds total")
            home_score, home_goals, home_behinds = self._parse_score(home_score_text)
            away_score, away_goals, away_behinds = self._parse_score(away_score_text)
            
            # Extract venue and date
            venue = cells[4].get_text(strip=True) if len(cells) > 4 else ""
            date_text = cells[5].get_text(strip=True) if len(cells) > 5 else ""
            
            # Parse date
            game_date = self._parse_date(date_text, season)
            
            return {
                'season': season,
                'round_number': round_num,
                'game_number': game_num,
                'home_team': home_team,
                'away_team': away_team,
                'home_score': home_score,
                'away_score': away_score,
                'home_goals': home_goals,
                'away_goals': away_goals,
                'home_behinds': home_behinds,
                'away_behinds': away_behinds,
                'venue': venue,
                'game_date': game_date,
                'is_finished': True
            }
            
        except Exception as e:
            logger.error(f"Error extracting game data: {e}")
            return None
    
    def _parse_score(self, score_text: str) -> tuple:
        """Parse score text to extract goals, behinds, and total"""
        try:
            if not score_text or score_text == '-':
                return 0, 0, 0
                
            # Format: "goals.behinds total" or just "total"
            parts = score_text.split()
            
            if len(parts) == 2:
                goals_behinds = parts[0].split('.')
                total = int(parts[1])
                
                if len(goals_behinds) == 2:
                    goals = int(goals_behinds[0])
                    behinds = int(goals_behinds[1])
                else:
                    goals = 0
                    behinds = 0
            else:
                total = int(score_text)
                goals = 0
                behinds = 0
                
            return total, goals, behinds
            
        except Exception as e:
            logger.error(f"Error parsing score '{score_text}': {e}")
            return 0, 0, 0
    
    def _parse_date(self, date_text: str, season: int) -> Optional[datetime]:
        """Parse date text to datetime object"""
        try:
            if not date_text:
                return None
                
            # Common AFL date formats
            date_formats = [
                "%d-%b-%Y",
                "%d/%m/%Y",
                "%d-%m-%Y",
                "%d %b %Y"
            ]
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_text, fmt)
                except ValueError:
                    continue
                    
            # If no format works, try to extract day and month and assume current year
            # This is a fallback for incomplete dates
            return None
            
        except Exception as e:
            logger.error(f"Error parsing date '{date_text}': {e}")
            return None
    
    def get_upcoming_games(self) -> List[Dict]:
        """Get upcoming games from AFL website"""
        # This would need to be implemented based on the current AFL website structure
        # For now, return empty list
        return []
    
    def save_games_to_db(self, db: Session, games: List[Dict]):
        """Save scraped games to database"""
        try:
            for game_data in games:
                # Check if game already exists
                existing_game = db.query(Game).filter(
                    Game.season == game_data['season'],
                    Game.round_number == game_data['round_number'],
                    Game.game_number == game_data['game_number']
                ).first()
                
                if not existing_game:
                    # Get or create teams
                    home_team = self._get_or_create_team(db, game_data['home_team'])
                    away_team = self._get_or_create_team(db, game_data['away_team'])
                    
                    # Create game
                    game = Game(
                        season=game_data['season'],
                        round_number=game_data['round_number'],
                        game_number=game_data['game_number'],
                        home_team_id=home_team.id,
                        away_team_id=away_team.id,
                        home_score=game_data['home_score'],
                        away_score=game_data['away_score'],
                        home_goals=game_data['home_goals'],
                        away_goals=game_data['away_goals'],
                        home_behinds=game_data['home_behinds'],
                        away_behinds=game_data['away_behinds'],
                        venue=game_data['venue'],
                        game_date=game_data['game_date'],
                        is_finished=game_data['is_finished']
                    )
                    
                    db.add(game)
                    
            db.commit()
            logger.info(f"Saved {len(games)} games to database")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving games to database: {e}")
            raise
    
    def _get_or_create_team(self, db: Session, team_name: str) -> Team:
        """Get existing team or create new one"""
        team = db.query(Team).filter(Team.name == team_name).first()
        
        if not team:
            # Create new team with basic info
            team = Team(
                name=team_name,
                abbreviation=self._get_team_abbreviation(team_name),
                city=self._extract_city_from_name(team_name),
                state=self._extract_state_from_name(team_name)
            )
            db.add(team)
            db.commit()
            db.refresh(team)
            
        return team
    
    def _get_team_abbreviation(self, team_name: str) -> str:
        """Get team abbreviation from name"""
        abbreviations = {
            'Adelaide': 'ADE',
            'Brisbane Lions': 'BRI',
            'Carlton': 'CAR',
            'Collingwood': 'COL',
            'Essendon': 'ESS',
            'Fremantle': 'FRE',
            'Geelong': 'GEE',
            'Gold Coast': 'GCS',
            'Greater Western Sydney': 'GWS',
            'Hawthorn': 'HAW',
            'Melbourne': 'MEL',
            'North Melbourne': 'NTH',
            'Port Adelaide': 'POR',
            'Richmond': 'RIC',
            'St Kilda': 'STK',
            'Sydney': 'SYD',
            'West Coast': 'WCE',
            'Western Bulldogs': 'WBD'
        }
        
        return abbreviations.get(team_name, team_name[:3].upper())
    
    def _extract_city_from_name(self, team_name: str) -> str:
        """Extract city from team name"""
        # This is a simplified version - would need more sophisticated parsing
        if 'Melbourne' in team_name:
            return 'Melbourne'
        elif 'Sydney' in team_name:
            return 'Sydney'
        elif 'Brisbane' in team_name:
            return 'Brisbane'
        elif 'Adelaide' in team_name:
            return 'Adelaide'
        elif 'Perth' in team_name or 'West Coast' in team_name:
            return 'Perth'
        else:
            return 'Unknown'
    
    def _extract_state_from_name(self, team_name: str) -> str:
        """Extract state from team name"""
        # Simplified state extraction
        if 'Melbourne' in team_name or 'Geelong' in team_name or 'Hawthorn' in team_name:
            return 'VIC'
        elif 'Sydney' in team_name:
            return 'NSW'
        elif 'Brisbane' in team_name or 'Gold Coast' in team_name:
            return 'QLD'
        elif 'Adelaide' in team_name or 'Port Adelaide' in team_name:
            return 'SA'
        elif 'West Coast' in team_name or 'Fremantle' in team_name:
            return 'WA'
        else:
            return 'Unknown' 