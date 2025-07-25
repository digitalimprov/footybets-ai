#!/usr/bin/env python3
"""
Comprehensive AFL Scraping Script

This script scrapes AFL data from afltables.com for multiple years
and saves it to the database in an AI-friendly format.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.scrapers.afl_scraper import AFLScraper
from app.core.database import SessionLocal, engine
from app.models.game import Game
from app.models.player import Player, PlayerGameStats
import argparse
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Comprehensive AFL Scraping')
    parser.add_argument('--start-year', type=int, default=2019, 
                       help='Starting year (default: 2019)')
    parser.add_argument('--end-year', type=int, default=2024, 
                       help='Ending year (default: 2024)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Run without saving to database')
    parser.add_argument('--test-only', action='store_true',
                       help='Test with just one round of current year')
    
    args = parser.parse_args()
    
    print("🏈 AFL Comprehensive Scraping Tool")
    print("=" * 50)
    
    if args.test_only:
        print("🧪 Running test mode (one round of current year)...")
        scraper = AFLScraper()
        result = scraper.test_small_scrape(season=2024, rounds=1)
        
        if result['success']:
            print(f"✅ Test successful!")
            print(f"📊 Games found: {result['games_found']}")
            print(f"🏆 Teams found: {result['teams_found']}")
            print(f"⏱️  Time taken: {result['time_taken']:.2f} seconds")
            
            # Show sample data
            if result['sample_games']:
                print("\n📋 Sample games:")
                for game in result['sample_games'][:3]:
                    print(f"  {game['home_team']} vs {game['away_team']} - Round {game['round']}")
                    print(f"    Score: {game['home_score']} - {game['away_score']}")
                    if 'venue' in game:
                        print(f"    Venue: {game['venue']}")
                    print()
        else:
            print(f"❌ Test failed: {result['error']}")
            return False
        
        return True
    
    # Check database connection
    try:
        db = SessionLocal()
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db.close()
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False
    
    # Run comprehensive scraping
    scraper = AFLScraper()
    
    save_to_db = not args.dry_run
    if args.dry_run:
        print("🔍 Running in dry-run mode (no database saves)")
    
    print(f"🚀 Starting comprehensive scraping for {args.start_year}-{args.end_year}...")
    
    result = scraper.scrape_multiple_seasons(
        start_year=args.start_year,
        end_year=args.end_year,
        save_to_db=save_to_db
    )
    
    if result['success']:
        print("\n🎉 Scraping completed successfully!")
        print(f"📊 Seasons processed: {result['seasons_processed']}")
        print(f"🎮 Total games: {result['total_games']}")
        print(f"👥 Total players: {result['total_players']}")
        print(f"📈 Total player stats: {result['total_player_stats']}")
        print(f"⏱️  Total time: {result['time_taken']:.1f} seconds")
        
        if result['season_details']:
            print("\n📋 Season breakdown:")
            for season in result['season_details']:
                print(f"  {season['year']}: {season['games']} games, "
                      f"{season['players']} players, "
                      f"{season['player_stats']} stats "
                      f"({season['time_taken']:.1f}s)")
        
        if result['errors']:
            print(f"\n⚠️  Errors encountered: {len(result['errors'])}")
            for error in result['errors']:
                print(f"   {error['year']}: {error['error']}")
        
        return True
    else:
        print(f"❌ Scraping failed!")
        if result['errors']:
            for error in result['errors']:
                print(f"   {error['year']}: {error['error']}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 