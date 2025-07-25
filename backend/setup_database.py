#!/usr/bin/env python3
"""
Database setup script for Footy Bets AI
Creates all necessary tables and adds sample AFL teams
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base
from app.models.team import Team
from app.models.game import Game
from app.models.prediction import Prediction
from app.models.user import User
from app.models.user_tip import UserTip
from app.models.analytics import Analytics
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    """Create all database tables"""
    logger.info("🔧 Setting up database tables...")
    
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating database tables: {e}")
        return False

def add_sample_teams():
    """Add sample AFL teams to the database"""
    logger.info("🏈 Adding sample AFL teams...")
    
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if teams already exist
        existing_teams = db.query(Team).count()
        if existing_teams > 0:
            logger.info(f"✅ {existing_teams} teams already exist in database")
            return True
        
        # Sample AFL teams
        teams_data = [
            {"name": "Carlton", "abbreviation": "CAR", "city": "Melbourne", "state": "VIC", "founded_year": 1864, "home_ground": "MCG"},
            {"name": "Collingwood", "abbreviation": "COL", "city": "Melbourne", "state": "VIC", "founded_year": 1892, "home_ground": "MCG"},
            {"name": "Essendon", "abbreviation": "ESS", "city": "Melbourne", "state": "VIC", "founded_year": 1872, "home_ground": "Marvel Stadium"},
            {"name": "Western Bulldogs", "abbreviation": "WB", "city": "Melbourne", "state": "VIC", "founded_year": 1877, "home_ground": "Marvel Stadium"},
            {"name": "Richmond", "abbreviation": "RIC", "city": "Melbourne", "state": "VIC", "founded_year": 1885, "home_ground": "MCG"},
            {"name": "Geelong", "abbreviation": "GEE", "city": "Geelong", "state": "VIC", "founded_year": 1859, "home_ground": "GMHBA Stadium"},
            {"name": "Hawthorn", "abbreviation": "HAW", "city": "Melbourne", "state": "VIC", "founded_year": 1902, "home_ground": "MCG"},
            {"name": "Melbourne", "abbreviation": "MEL", "city": "Melbourne", "state": "VIC", "founded_year": 1858, "home_ground": "MCG"},
            {"name": "St Kilda", "abbreviation": "STK", "city": "Melbourne", "state": "VIC", "founded_year": 1873, "home_ground": "Marvel Stadium"},
            {"name": "North Melbourne", "abbreviation": "NM", "city": "Melbourne", "state": "VIC", "founded_year": 1869, "home_ground": "Marvel Stadium"},
            {"name": "Sydney", "abbreviation": "SYD", "city": "Sydney", "state": "NSW", "founded_year": 1874, "home_ground": "SCG"},
            {"name": "Brisbane Lions", "abbreviation": "BRI", "city": "Brisbane", "state": "QLD", "founded_year": 1996, "home_ground": "Gabba"},
            {"name": "Adelaide", "abbreviation": "ADE", "city": "Adelaide", "state": "SA", "founded_year": 1990, "home_ground": "Adelaide Oval"},
            {"name": "Port Adelaide", "abbreviation": "PA", "city": "Adelaide", "state": "SA", "founded_year": 1870, "home_ground": "Adelaide Oval"},
            {"name": "West Coast", "abbreviation": "WCE", "city": "Perth", "state": "WA", "founded_year": 1986, "home_ground": "Optus Stadium"},
            {"name": "Fremantle", "abbreviation": "FRE", "city": "Perth", "state": "WA", "founded_year": 1994, "home_ground": "Optus Stadium"},
            {"name": "Gold Coast", "abbreviation": "GCS", "city": "Gold Coast", "state": "QLD", "founded_year": 2009, "home_ground": "Metricon Stadium"},
            {"name": "Greater Western Sydney", "abbreviation": "GWS", "city": "Sydney", "state": "NSW", "founded_year": 2009, "home_ground": "Giants Stadium"}
        ]
        
        for team_data in teams_data:
            team = Team(**team_data)
            db.add(team)
        
        db.commit()
        logger.info(f"✅ Added {len(teams_data)} AFL teams to database")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error adding teams: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def add_sample_games():
    """Add sample games for testing"""
    logger.info("🏟️ Adding sample games...")
    
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if games already exist
        existing_games = db.query(Game).count()
        if existing_games > 0:
            logger.info(f"✅ {existing_games} games already exist in database")
            return True
        
        # Get teams
        carlton = db.query(Team).filter(Team.name == "Carlton").first()
        collingwood = db.query(Team).filter(Team.name == "Collingwood").first()
        essendon = db.query(Team).filter(Team.name == "Essendon").first()
        bulldogs = db.query(Team).filter(Team.name == "Western Bulldogs").first()
        
        if not all([carlton, collingwood, essendon, bulldogs]):
            logger.error("❌ Required teams not found in database")
            return False
        
        # Tonight's games
        tonight = datetime.now().replace(hour=19, minute=30, second=0, microsecond=0)
        
        games_data = [
            {
                "season": 2024,
                "round_number": 18,
                "game_number": 1,
                "home_team_id": carlton.id,
                "away_team_id": collingwood.id,
                "venue": "MCG",
                "game_date": tonight,
                "is_finished": False,
                "weather": "Partly cloudy",
                "temperature": 15.0
            },
            {
                "season": 2024,
                "round_number": 18,
                "game_number": 2,
                "home_team_id": essendon.id,
                "away_team_id": bulldogs.id,
                "venue": "Marvel Stadium",
                "game_date": tonight + timedelta(minutes=20),
                "is_finished": False,
                "weather": "Clear",
                "temperature": 14.0
            }
        ]
        
        for game_data in games_data:
            game = Game(**game_data)
            db.add(game)
        
        db.commit()
        logger.info(f"✅ Added {len(games_data)} sample games to database")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error adding games: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def main():
    """Main setup function"""
    logger.info("🚀 Starting Footy Bets AI Database Setup")
    logger.info("=" * 50)
    
    # Step 1: Create tables
    if not setup_database():
        logger.error("❌ Failed to create database tables")
        return False
    
    # Step 2: Add sample teams
    if not add_sample_teams():
        logger.error("❌ Failed to add sample teams")
        return False
    
    # Step 3: Add sample games
    if not add_sample_games():
        logger.error("❌ Failed to add sample games")
        return False
    
    logger.info("\n🎉 Database setup completed successfully!")
    logger.info("✅ All tables created")
    logger.info("✅ Sample AFL teams added")
    logger.info("✅ Sample games added")
    logger.info("\n🚀 Your Footy Bets AI database is ready!")
    
    return True

if __name__ == "__main__":
    main() 