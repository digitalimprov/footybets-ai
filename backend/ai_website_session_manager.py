#!/usr/bin/env python3
"""
Website AI Session Manager
Comprehensive session management for all AI interactions across the website
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

from ai_session_manager import AISessionManager
from gemini_session_learning_analyzer import SessionLearningGeminiAnalyzer
from ai_content_generator import AIContentGenerator

@dataclass
class WebsiteSession:
    """Website session data structure"""
    session_id: str
    user_id: Optional[str]
    start_time: str
    last_activity: str
    ai_interactions: int
    features_used: List[str]
    learning_progress: Dict[str, int]

@dataclass
class UserInteraction:
    """User interaction with AI features"""
    timestamp: str
    user_id: Optional[str]
    feature: str
    action: str
    input_data: Dict
    response_data: Dict
    feedback_rating: Optional[int]
    feedback_comment: Optional[str]

class WebsiteAISessionManager:
    """Comprehensive AI session manager for the entire website"""
    
    def __init__(self, api_key: Optional[str] = None, session_dir: str = "website_ai_sessions"):
        """Initialize Website AI Session Manager"""
        # Initialize core AI session manager
        self.ai_session_manager = AISessionManager(api_key, session_dir)
        
        # Initialize specialized analyzers
        self.brownlow_analyzer = SessionLearningGeminiAnalyzer(api_key)
        self.content_generator = AIContentGenerator(api_key)
        
        # Website-specific session management
        self.session_dir = session_dir
        os.makedirs(session_dir, exist_ok=True)
        
        # Website session data
        self.website_sessions: Dict[str, WebsiteSession] = {}
        self.user_interactions: List[UserInteraction] = []
        self.feature_usage_stats: Dict[str, Dict] = {}
        
        # Load existing website sessions
        self.load_website_sessions()
        
        print(f"🌐 Website AI Session Manager initialized")
        print(f"🤖 Core AI Session: {self.ai_session_manager.session_id}")
        print(f"📊 Website Sessions: {len(self.website_sessions)}")
    
    def load_website_sessions(self):
        """Load existing website session data"""
        sessions_file = os.path.join(self.session_dir, "website_sessions.json")
        
        try:
            if os.path.exists(sessions_file):
                with open(sessions_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Load website sessions
                for session_data in data.get('website_sessions', []):
                    session = WebsiteSession(**session_data)
                    self.website_sessions[session.session_id] = session
                
                # Load user interactions
                for interaction_data in data.get('user_interactions', []):
                    interaction = UserInteraction(**interaction_data)
                    self.user_interactions.append(interaction)
                
                # Load feature usage stats
                self.feature_usage_stats = data.get('feature_usage_stats', {})
                
                print(f"✅ Loaded {len(self.website_sessions)} website sessions")
                print(f"✅ Loaded {len(self.user_interactions)} user interactions")
                return True
        except Exception as e:
            print(f"⚠️  Could not load website sessions: {str(e)}")
        
        return False
    
    def save_website_sessions(self):
        """Save website session data"""
        try:
            sessions_file = os.path.join(self.session_dir, "website_sessions.json")
            
            data = {
                'website_sessions': [asdict(session) for session in self.website_sessions.values()],
                'user_interactions': [asdict(interaction) for interaction in self.user_interactions[-1000:]],  # Last 1000
                'feature_usage_stats': self.feature_usage_stats,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(sessions_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            
            print(f"💾 Website sessions saved: {len(self.website_sessions)} sessions")
            return True
        except Exception as e:
            print(f"❌ Could not save website sessions: {str(e)}")
            return False
    
    def create_website_session(self, user_id: Optional[str] = None) -> str:
        """Create a new website session"""
        session_id = f"website_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session = WebsiteSession(
            session_id=session_id,
            user_id=user_id,
            start_time=datetime.now().isoformat(),
            last_activity=datetime.now().isoformat(),
            ai_interactions=0,
            features_used=[],
            learning_progress={}
        )
        
        self.website_sessions[session_id] = session
        print(f"🆕 Created website session: {session_id}")
        
        return session_id
    
    def record_user_interaction(self, session_id: str, user_id: Optional[str], 
                              feature: str, action: str, input_data: Dict, 
                              response_data: Dict, feedback_rating: Optional[int] = None,
                              feedback_comment: Optional[str] = None):
        """Record a user interaction with AI features"""
        # Update website session
        if session_id in self.website_sessions:
            session = self.website_sessions[session_id]
            session.last_activity = datetime.now().isoformat()
            session.ai_interactions += 1
            
            if feature not in session.features_used:
                session.features_used.append(feature)
            
            if feature not in session.learning_progress:
                session.learning_progress[feature] = 0
            session.learning_progress[feature] += 1
        
        # Record interaction
        interaction = UserInteraction(
            timestamp=datetime.now().isoformat(),
            user_id=user_id,
            feature=feature,
            action=action,
            input_data=input_data,
            response_data=response_data,
            feedback_rating=feedback_rating,
            feedback_comment=feedback_comment
        )
        
        self.user_interactions.append(interaction)
        
        # Update feature usage stats
        if feature not in self.feature_usage_stats:
            self.feature_usage_stats[feature] = {
                'total_interactions': 0,
                'unique_users': set(),
                'average_rating': 0,
                'total_ratings': 0
            }
        
        self.feature_usage_stats[feature]['total_interactions'] += 1
        if user_id:
            self.feature_usage_stats[feature]['unique_users'].add(user_id)
        
        if feedback_rating:
            stats = self.feature_usage_stats[feature]
            stats['total_ratings'] += 1
            stats['average_rating'] = (
                (stats['average_rating'] * (stats['total_ratings'] - 1) + feedback_rating) / 
                stats['total_ratings']
            )
        
        print(f"📝 Recorded {feature} interaction: {action}")
    
    def analyze_brownlow_with_session(self, session_id: str, user_id: Optional[str], 
                                    season: int, learning_seasons: List[int] = None) -> Dict:
        """Analyze Brownlow with session learning and interaction recording"""
        print(f"🏆 Analyzing Brownlow for session {session_id}")
        
        # Record interaction start
        self.record_user_interaction(
            session_id=session_id,
            user_id=user_id,
            feature='brownlow',
            action='analyze_season',
            input_data={'season': season, 'learning_seasons': learning_seasons},
            response_data={}
        )
        
        # Perform analysis
        start_time = time.time()
        results = self.brownlow_analyzer.analyze_season_brownlow(season, learning_seasons)
        analysis_time = time.time() - start_time
        
        # Record successful interaction
        self.record_user_interaction(
            session_id=session_id,
            user_id=user_id,
            feature='brownlow',
            action='analysis_complete',
            input_data={'season': season},
            response_data={
                'success': True,
                'analysis_time': analysis_time,
                'total_games': results.get('total_games', 0),
                'predicted_winner': results.get('winner', {}).get('player_name', 'Unknown')
            }
        )
        
        return results
    
    def generate_content_with_session(self, session_id: str, user_id: Optional[str],
                                    content_type: str, content_data: Dict) -> Dict:
        """Generate content with session learning and interaction recording"""
        print(f"📝 Generating {content_type} content for session {session_id}")
        
        # Record interaction start
        self.record_user_interaction(
            session_id=session_id,
            user_id=user_id,
            feature='content',
            action=f'generate_{content_type}',
            input_data=content_data,
            response_data={}
        )
        
        # Generate content based on type
        if content_type == 'brownlow':
            result = self.content_generator.generate_brownlow_content(content_data)
        elif content_type == 'predictions':
            result = self.content_generator.generate_prediction_content(content_data)
        elif content_type == 'analytics':
            result = self.content_generator.generate_analytics_content(
                content_data.get('data', {}), 
                content_data.get('analysis_type', 'general')
            )
        elif content_type == 'team_analysis':
            result = self.content_generator.generate_team_analysis_content(content_data)
        elif content_type == 'player_profile':
            result = self.content_generator.generate_player_profile_content(content_data)
        elif content_type == 'match_preview':
            result = self.content_generator.generate_match_preview_content(content_data)
        else:
            result = {'success': False, 'error': f'Unknown content type: {content_type}'}
        
        # Record successful interaction
        self.record_user_interaction(
            session_id=session_id,
            user_id=user_id,
            feature='content',
            action=f'{content_type}_generated',
            input_data=content_data,
            response_data={
                'success': result.get('success', False),
                'content_type': content_type,
                'session_context_used': result.get('session_context_used', 0)
            }
        )
        
        return result
    
    def add_feedback_with_session(self, session_id: str, user_id: Optional[str],
                                feature: str, prediction: Dict, feedback: str, rating: int):
        """Add feedback with session learning and interaction recording"""
        print(f"📝 Adding feedback for {feature} in session {session_id}")
        
        # Add feedback to AI session manager
        self.ai_session_manager.add_feedback(feature, prediction, feedback, rating)
        
        # Record feedback interaction
        self.record_user_interaction(
            session_id=session_id,
            user_id=user_id,
            feature=feature,
            action='add_feedback',
            input_data={'prediction': prediction, 'feedback': feedback, 'rating': rating},
            response_data={'success': True},
            feedback_rating=rating,
            feedback_comment=feedback
        )
    
    def get_website_session_stats(self) -> Dict:
        """Get comprehensive website session statistics"""
        stats = {
            'total_website_sessions': len(self.website_sessions),
            'total_user_interactions': len(self.user_interactions),
            'active_sessions': len([s for s in self.website_sessions.values() 
                                  if (datetime.now() - datetime.fromisoformat(s.last_activity.replace('Z', '+00:00'))).days < 1]),
            'feature_usage': {},
            'ai_session_stats': self.ai_session_manager.get_session_stats(),
            'learning_progress': {}
        }
        
        # Feature usage breakdown
        for feature, feature_stats in self.feature_usage_stats.items():
            stats['feature_usage'][feature] = {
                'total_interactions': feature_stats['total_interactions'],
                'unique_users': len(feature_stats['unique_users']),
                'average_rating': round(feature_stats['average_rating'], 2),
                'total_ratings': feature_stats['total_ratings']
            }
        
        # Learning progress by feature
        for session in self.website_sessions.values():
            for feature, progress in session.learning_progress.items():
                if feature not in stats['learning_progress']:
                    stats['learning_progress'][feature] = 0
                stats['learning_progress'][feature] += progress
        
        return stats
    
    def get_user_session_history(self, user_id: str) -> Dict:
        """Get session history for a specific user"""
        user_sessions = [s for s in self.website_sessions.values() if s.user_id == user_id]
        user_interactions = [i for i in self.user_interactions if i.user_id == user_id]
        
        return {
            'user_id': user_id,
            'total_sessions': len(user_sessions),
            'total_interactions': len(user_interactions),
            'features_used': list(set([i.feature for i in user_interactions])),
            'recent_interactions': [
                {
                    'timestamp': i.timestamp,
                    'feature': i.feature,
                    'action': i.action,
                    'rating': i.feedback_rating
                }
                for i in sorted(user_interactions, key=lambda x: x.timestamp, reverse=True)[:10]
            ],
            'session_history': [
                {
                    'session_id': s.session_id,
                    'start_time': s.start_time,
                    'ai_interactions': s.ai_interactions,
                    'features_used': s.features_used
                }
                for s in sorted(user_sessions, key=lambda x: x.start_time, reverse=True)
            ]
        }
    
    def export_session_data(self, filename: str = None) -> str:
        """Export comprehensive session data for analysis"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"website_ai_session_export_{timestamp}.json"
        
        export_data = {
            'website_session_stats': self.get_website_session_stats(),
            'website_sessions': [asdict(s) for s in self.website_sessions.values()],
            'user_interactions': [asdict(i) for i in self.user_interactions[-1000:]],  # Last 1000
            'feature_usage_stats': self.feature_usage_stats,
            'ai_session_export': self.ai_session_manager.export_session_data()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        print(f"📊 Website session data exported to: {filename}")
        return filename
    
    def save_all_sessions(self):
        """Save all session data"""
        # Save AI session
        self.ai_session_manager.save_session()
        
        # Save website sessions
        self.save_website_sessions()
        
        print("💾 All session data saved")

def main():
    """Test the Website AI Session Manager"""
    print("🌐 Website AI Session Manager Test")
    print("=" * 60)
    
    try:
        # Initialize website session manager
        website_manager = WebsiteAISessionManager()
        
        # Create a test session
        session_id = website_manager.create_website_session(user_id="test_user_123")
        
        # Test Brownlow analysis with session
        print(f"\n🏆 Testing Brownlow analysis with session {session_id}...")
        brownlow_result = website_manager.analyze_brownlow_with_session(
            session_id=session_id,
            user_id="test_user_123",
            season=2024,
            learning_seasons=[2022, 2023]
        )
        
        print(f"✅ Brownlow analysis: {brownlow_result.get('success', False)}")
        
        # Test content generation with session
        print(f"\n📝 Testing content generation with session {session_id}...")
        content_data = {
            'season': 2024,
            'winner': {
                'player_name': 'Marcus Bontempelli',
                'team': 'Western Bulldogs',
                'votes': 28
            }
        }
        
        content_result = website_manager.generate_content_with_session(
            session_id=session_id,
            user_id="test_user_123",
            content_type='brownlow',
            content_data=content_data
        )
        
        print(f"✅ Content generation: {content_result.get('success', False)}")
        
        # Test feedback with session
        print(f"\n📝 Testing feedback with session {session_id}...")
        website_manager.add_feedback_with_session(
            session_id=session_id,
            user_id="test_user_123",
            feature='brownlow',
            prediction={'votes': [{'player_name': 'Test Player', 'votes': 3}]},
            feedback='Great prediction!',
            rating=5
        )
        
        # Show comprehensive stats
        print(f"\n📊 Website Session Statistics:")
        stats = website_manager.get_website_session_stats()
        print(f"  Total website sessions: {stats['total_website_sessions']}")
        print(f"  Total user interactions: {stats['total_user_interactions']}")
        print(f"  Active sessions: {stats['active_sessions']}")
        
        for feature, usage in stats['feature_usage'].items():
            print(f"  {feature}: {usage['total_interactions']} interactions, {usage['unique_users']} users")
        
        # Save all sessions
        website_manager.save_all_sessions()
        print(f"\n💾 All sessions saved for future resumption")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 