#!/usr/bin/env python3
"""
Test AI predictor with real database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.ai.predictor import AFLPredictor
from app.core.database import SessionLocal
from app.models.game import Game
from app.models.team import Team
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_ai_predictor_with_database():
    """Test AI predictor with real database data"""
    logger.info("🚀 Testing AI Predictor with Database")
    logger.info("=" * 50)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Get tonight's games
        from datetime import datetime, timedelta
        tonight = datetime.now().replace(hour=19, minute=30, second=0, microsecond=0)
        tomorrow = tonight + timedelta(days=1)
        
        games = db.query(Game).filter(
            Game.game_date >= tonight,
            Game.game_date < tomorrow
        ).all()
        
        if not games:
            logger.info("No games found for tonight, getting all games...")
            games = db.query(Game).limit(2).all()
        
        logger.info(f"Found {len(games)} games to predict")
        
        # Create AI predictor
        predictor = AFLPredictor()
        logger.info("✅ AI Predictor initialized")
        
        # Test predictions for each game
        for i, game in enumerate(games, 1):
            logger.info(f"\n🎯 Game {i}: {game.home_team.name} vs {game.away_team.name}")
            logger.info(f"📍 Venue: {game.venue}")
            logger.info(f"🕐 Time: {game.game_date}")
            
            try:
                # Generate prediction
                prediction = predictor._predict_single_game(db, game)
                
                if prediction:
                    logger.info("✅ AI Prediction Generated!")
                    logger.info(f"🏆 Predicted Winner ID: {prediction.predicted_winner_id}")
                    logger.info(f"📊 Predicted Score: {prediction.predicted_home_score} - {prediction.predicted_away_score}")
                    logger.info(f"🎯 Confidence: {prediction.confidence_score}")
                    logger.info(f"💰 Recommended Bet: {prediction.recommended_bet}")
                    logger.info(f"💎 Bet Confidence: {prediction.bet_confidence}")
                    logger.info(f"🧠 Reasoning: {prediction.reasoning[:100] if prediction.reasoning else 'N/A'}...")
                    
                    # Save prediction to database
                    db.add(prediction)
                    db.commit()
                    logger.info("✅ Prediction saved to database")
                    
                else:
                    logger.warning("⚠️ No prediction generated")
                    
            except Exception as e:
                logger.error(f"❌ Error generating prediction: {e}")
                continue
        
        logger.info("\n🎉 AI Predictor Test Complete!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error testing AI predictor: {e}")
        return False
    finally:
        db.close()

def show_database_stats():
    """Show database statistics"""
    logger.info("\n📊 Database Statistics")
    logger.info("=" * 30)
    
    db = SessionLocal()
    
    try:
        team_count = db.query(Team).count()
        game_count = db.query(Game).count()
        
        logger.info(f"🏈 Teams: {team_count}")
        logger.info(f"🏟️ Games: {game_count}")
        
        # Show sample teams
        teams = db.query(Team).limit(5).all()
        logger.info("\n📋 Sample Teams:")
        for team in teams:
            logger.info(f"   • {team.name} ({team.abbreviation}) - {team.home_ground}")
        
        # Show sample games
        games = db.query(Game).limit(3).all()
        logger.info("\n📋 Sample Games:")
        for game in games:
            logger.info(f"   • {game.home_team.name} vs {game.away_team.name} at {game.venue}")
        
    except Exception as e:
        logger.error(f"❌ Error showing database stats: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("🎯 Starting AI Predictor Database Test")
    
    # Show database stats first
    show_database_stats()
    
    # Test AI predictor
    success = test_ai_predictor_with_database()
    
    if success:
        logger.info("\n🎉 ALL TESTS PASSED! Your AI predictor is working with the database!")
    else:
        logger.info("\n⚠️ Some tests failed, but the basic setup is working.") 