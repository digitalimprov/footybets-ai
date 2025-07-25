#!/usr/bin/env python3
"""
Universal AI Content Generator with Session Learning
Uses centralized session manager for consistent learning across all content types
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List, Optional
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_session_manager import AISessionManager
from ai_content_style_guide import AI_CONTENT_STYLE_GUIDE

class AIContentGenerator:
    """Universal AI content generator with session learning"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize AI Content Generator"""
        # Use centralized session manager
        self.session_manager = AISessionManager(api_key)
        
        print(f"🤖 Initialized AI Content Generator with session: {self.session_manager.session_id}")
    
    def generate_brownlow_content(self, season_data: Dict, round_data: Dict = None) -> Dict:
        """Generate Brownlow Medal content with session learning"""
        if round_data:
            # Generate round-specific content
            prompt = f"""
Generate engaging Brownlow Medal content for {season_data['season']} Round {round_data['round']}.

Season Context:
- Season: {season_data['season']}
- Current Round: {round_data['round']}
- Games in Round: {len(round_data['games'])}

Round Results:
{json.dumps(round_data, indent=2)}

Style Requirements:
{AI_CONTENT_STYLE_GUIDE}

Create content that includes:
1. Round summary with key performances
2. Brownlow vote analysis for each game
3. Player highlights and standout performances
4. Season implications for Brownlow race
5. SEO-friendly headings and keywords
6. Engaging, witty tone for AFL betting enthusiasts

Format as HTML with proper structure and SEO elements.
"""
        else:
            # Generate season overview content
            prompt = f"""
Generate comprehensive Brownlow Medal season overview for {season_data['season']}.

Season Data:
{json.dumps(season_data, indent=2)}

Style Requirements:
{AI_CONTENT_STYLE_GUIDE}

Create content that includes:
1. Season summary and key storylines
2. Top contenders analysis
3. Player performance highlights
4. Round-by-round vote breakdown
5. Historical context and comparisons
6. SEO-friendly structure with keywords
7. Engaging, witty tone for AFL betting enthusiasts

Format as HTML with proper structure and SEO elements.
"""
        
        result = self.session_manager.generate_ai_response('content', prompt, season_data)
        
        if result['success']:
            return {
                'success': True,
                'content': result['response'],
                'content_type': 'brownlow',
                'season': season_data['season'],
                'round': round_data['round'] if round_data else None,
                'session_context_used': result['session_context_used']
            }
        else:
            return {
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'content_type': 'brownlow'
            }
    
    def generate_prediction_content(self, prediction_data: Dict) -> Dict:
        """Generate prediction content with session learning"""
        prompt = f"""
Generate engaging prediction content for AFL betting analysis.

Prediction Data:
{json.dumps(prediction_data, indent=2)}

Style Requirements:
{AI_CONTENT_STYLE_GUIDE}

Create content that includes:
1. Match analysis and key factors
2. Player form and statistics
3. Head-to-head history
4. Prediction with confidence level
5. Betting insights and considerations
6. SEO-friendly structure
7. Engaging, witty tone for AFL betting enthusiasts

Format as HTML with proper structure and SEO elements.
"""
        
        result = self.session_manager.generate_ai_response('predictions', prompt, prediction_data)
        
        if result['success']:
            return {
                'success': True,
                'content': result['response'],
                'content_type': 'predictions',
                'session_context_used': result['session_context_used']
            }
        else:
            return {
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'content_type': 'predictions'
            }
    
    def generate_analytics_content(self, analytics_data: Dict, analysis_type: str) -> Dict:
        """Generate analytics content with session learning"""
        prompt = f"""
Generate insightful analytics content for {analysis_type} analysis.

Analytics Data:
{json.dumps(analytics_data, indent=2)}

Style Requirements:
{AI_CONTENT_STYLE_GUIDE}

Create content that includes:
1. Data analysis and key findings
2. Statistical insights and patterns
3. Performance trends and comparisons
4. Actionable insights for betting
5. Visual data interpretation
6. SEO-friendly structure
7. Engaging, witty tone for AFL betting enthusiasts

Format as HTML with proper structure and SEO elements.
"""
        
        result = self.session_manager.generate_ai_response('analytics', prompt, analytics_data)
        
        if result['success']:
            return {
                'success': True,
                'content': result['response'],
                'content_type': 'analytics',
                'analysis_type': analysis_type,
                'session_context_used': result['session_context_used']
            }
        else:
            return {
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'content_type': 'analytics'
            }
    
    def generate_team_analysis_content(self, team_data: Dict) -> Dict:
        """Generate team analysis content with session learning"""
        prompt = f"""
Generate comprehensive team analysis content.

Team Data:
{json.dumps(team_data, indent=2)}

Style Requirements:
{AI_CONTENT_STYLE_GUIDE}

Create content that includes:
1. Team performance analysis
2. Key player statistics and form
3. Tactical analysis and style
4. Recent form and trends
5. Strengths and weaknesses
6. Betting implications
7. SEO-friendly structure
8. Engaging, witty tone for AFL betting enthusiasts

Format as HTML with proper structure and SEO elements.
"""
        
        result = self.session_manager.generate_ai_response('content', prompt, team_data)
        
        if result['success']:
            return {
                'success': True,
                'content': result['response'],
                'content_type': 'team_analysis',
                'team': team_data.get('team_name', 'Unknown'),
                'session_context_used': result['session_context_used']
            }
        else:
            return {
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'content_type': 'team_analysis'
            }
    
    def generate_player_profile_content(self, player_data: Dict) -> Dict:
        """Generate player profile content with session learning"""
        prompt = f"""
Generate engaging player profile content.

Player Data:
{json.dumps(player_data, indent=2)}

Style Requirements:
{AI_CONTENT_STYLE_GUIDE}

Create content that includes:
1. Player background and career highlights
2. Current season performance analysis
3. Statistical breakdown and trends
4. Playing style and strengths
5. Brownlow Medal prospects
6. Betting value and considerations
7. SEO-friendly structure
8. Engaging, witty tone for AFL betting enthusiasts

Format as HTML with proper structure and SEO elements.
"""
        
        result = self.session_manager.generate_ai_response('content', prompt, player_data)
        
        if result['success']:
            return {
                'success': True,
                'content': result['response'],
                'content_type': 'player_profile',
                'player': player_data.get('player_name', 'Unknown'),
                'session_context_used': result['session_context_used']
            }
        else:
            return {
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'content_type': 'player_profile'
            }
    
    def generate_match_preview_content(self, match_data: Dict) -> Dict:
        """Generate match preview content with session learning"""
        prompt = f"""
Generate comprehensive match preview content.

Match Data:
{json.dumps(match_data, indent=2)}

Style Requirements:
{AI_CONTENT_STYLE_GUIDE}

Create content that includes:
1. Match context and importance
2. Team form and recent performance
3. Key player matchups and statistics
4. Head-to-head history
5. Tactical analysis and predictions
6. Betting insights and odds analysis
7. SEO-friendly structure
8. Engaging, witty tone for AFL betting enthusiasts

Format as HTML with proper structure and SEO elements.
"""
        
        result = self.session_manager.generate_ai_response('content', prompt, match_data)
        
        if result['success']:
            return {
                'success': True,
                'content': result['response'],
                'content_type': 'match_preview',
                'home_team': match_data.get('home_team', 'Unknown'),
                'away_team': match_data.get('away_team', 'Unknown'),
                'session_context_used': result['session_context_used']
            }
        else:
            return {
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'content_type': 'match_preview'
            }
    
    def add_content_feedback(self, content_id: str, content_type: str, feedback: str, rating: int):
        """Add feedback for content generation to improve learning"""
        self.session_manager.add_feedback(content_type, {'content_id': content_id}, feedback, rating)
    
    def get_content_generation_stats(self) -> Dict:
        """Get statistics for content generation"""
        stats = self.session_manager.get_session_stats()
        
        # Filter for content-related metrics
        content_stats = {
            'total_content_generated': len([msg for msg in self.session_manager.conversation_history if msg.ai_feature == 'content']),
            'content_learning_examples': len([ex for ex in self.session_manager.learning_examples if ex.ai_feature == 'content']),
            'content_performance_metrics': len([m for m in self.session_manager.performance_metrics if m.feature == 'content']),
            'session_id': self.session_manager.session_id
        }
        
        return content_stats
    
    def save_session(self):
        """Save current session data"""
        return self.session_manager.save_session()

def main():
    """Test the AI Content Generator"""
    print("🤖 AI Content Generator Test")
    print("=" * 50)
    
    try:
        # Initialize content generator
        generator = AIContentGenerator()
        
        # Test Brownlow content generation
        print("\n🏆 Testing Brownlow content generation...")
        season_data = {
            'season': 2024,
            'winner': {
                'player_name': 'Marcus Bontempelli',
                'team': 'Western Bulldogs',
                'votes': 28
            },
            'player_standings': [
                {
                    'rank': 1,
                    'player_name': 'Marcus Bontempelli',
                    'team': 'Western Bulldogs',
                    'total_votes': 28
                }
            ]
        }
        
        result = generator.generate_brownlow_content(season_data)
        print(f"✅ Brownlow content generation: {result['success']}")
        
        # Test prediction content generation
        print("\n🎯 Testing prediction content generation...")
        prediction_data = {
            'match': 'Sydney vs Melbourne',
            'prediction': 'Sydney by 15 points',
            'confidence': 'High',
            'key_factors': ['Home advantage', 'Recent form', 'Key player availability']
        }
        
        pred_result = generator.generate_prediction_content(prediction_data)
        print(f"✅ Prediction content generation: {pred_result['success']}")
        
        # Show content generation stats
        print("\n📊 Content Generation Statistics:")
        stats = generator.get_content_generation_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Save session
        generator.save_session()
        print(f"\n💾 Session saved for future resumption")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 