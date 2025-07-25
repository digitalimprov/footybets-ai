#!/usr/bin/env python3
"""
Production script to scrape 5 years of AFL data (2020-2025) and save to database
"""

import sys
import os
import time
import re
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.scrapers.afl_scraper import AFLScraper
from app.core.database import SessionLocal, engine
from app.models.game import Game
from app.models.team import Team
from app.models.player import Player, PlayerGameStats
from sqlalchemy.orm import sessionmaker

def scrape_afl_data_to_database():
    """Scrape last 5 years (2020-2025) and save to database in AI-friendly format"""
    print("🏈 AFL Data Collection - Production Run")
    print("=" * 60)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Create database session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        scraper = AFLScraper()
        
        # Define seasons to scrape
        seasons = [2020, 2021, 2022, 2023, 2024, 2025]
        
        total_games_saved = 0
        total_player_stats_saved = 0
        total_teams_saved = 0
        total_players_saved = 0
        
        overall_start_time = time.time()
        
        for season in seasons:
            print(f"\n📊 Processing {season} season...")
            season_start_time = time.time()
            
            # Scrape season data
            result = scraper.parse_season_page(season)
            
            if not result['success']:
                print(f"❌ Failed to scrape {season} season: {result['error']}")
                continue
            
            games = result['games']
            
            # Filter to only completed games
            completed_games = []
            for game in games:
                if game['home_score'] > 0 or game['away_score'] > 0:
                    # Fix round numbers for 2024 and 2025 seasons (Round 0 adjustment)
                    # AFL introduced Round 0 in 2024 and 2025, so we need to adjust:
                    # - Round 1 from scraper becomes Round 0 in database
                    # - Round 2 from scraper becomes Round 1 in database, etc.
                    original_round = game.get('round')
                    if season in [2024, 2025] and original_round:
                        game['round'] = original_round - 1
                        game['game_id'] = f"{season}_r{game['round']}_{game['home_team']}_{game['away_team']}"
                    
                    completed_games.append(game)
            
            print(f"  ✅ Found {len(completed_games)} completed games")
            
            # Show round adjustment info for 2024/2025
            if season in [2024, 2025]:
                print(f"  📋 Note: Round numbers adjusted for {season} (Round 0 format)")
                # Show sample of round adjustments
                sample_games = completed_games[:3]
                for game in sample_games:
                    print(f"    - {game['home_team']} vs {game['away_team']}: Round {game['round']}")
            
            # Get or create teams
            teams_cache = {}
            for game in completed_games:
                for team_name in [game['home_team'], game['away_team']]:
                    if team_name not in teams_cache:
                        team = db.query(Team).filter(Team.name == team_name).first()
                        if not team:
                            team = Team(name=team_name)
                            db.add(team)
                            db.flush()  # Get the ID
                            total_teams_saved += 1
                            print(f"    🏆 Created new team: {team_name}")
                        teams_cache[team_name] = team
            
            # Save games and fetch player stats
            games_with_stats = 0
            for i, game_data in enumerate(completed_games):
                if i % 10 == 0:  # Progress update every 10 games
                    print(f"  📝 Processing game {i+1}/{len(completed_games)}: {game_data['home_team']} vs {game_data['away_team']}")
                
                # Create or get game record
                existing_game = db.query(Game).filter(
                    Game.season == season,
                    Game.round_number == game_data['round'],
                    Game.home_team_id == teams_cache[game_data['home_team']].id,
                    Game.away_team_id == teams_cache[game_data['away_team']].id
                ).first()
                
                if existing_game:
                    # Update existing game
                    game_record = existing_game
                    game_record.home_score = game_data['home_score']
                    game_record.away_score = game_data['away_score']
                    game_record.venue = game_data.get('venue')
                    game_record.game_date = game_data.get('game_date')
                    game_record.is_finished = True
                else:
                    # Create new game
                    game_record = Game(
                        season=season,
                        round_number=game_data['round'],
                        home_team_id=teams_cache[game_data['home_team']].id,
                        away_team_id=teams_cache[game_data['away_team']].id,
                        home_score=game_data['home_score'],
                        away_score=game_data['away_score'],
                        venue=game_data.get('venue'),
                        game_date=game_data.get('game_date'),
                        is_finished=True
                    )
                    db.add(game_record)
                    db.flush()  # Get the ID
                    total_games_saved += 1
                
                # Fetch player statistics if available
                if game_data.get('stats_link'):
                    stats_link = game_data['stats_link']
                    if '/stats/games/' in stats_link:
                        game_id_match = re.search(r'/stats/games/\d+/(\d+)\.html', stats_link)
                        if game_id_match:
                            game_id = game_id_match.group(1)
                            
                            # Fetch player statistics
                            stats_result = scraper.parse_game_stats(game_id, season)
                            if stats_result['success']:
                                games_with_stats += 1
                                
                                # Save player statistics
                                for team_name, players in stats_result['player_stats'].items():
                                    team_record = teams_cache[team_name]
                                    
                                    for player_data in players:
                                        # Get or create player
                                        player_name = player_data['name']
                                        player = db.query(Player).filter(Player.name == player_name).first()
                                        
                                        if not player:
                                            player = Player(
                                                name=player_name,
                                                current_team_id=team_record.id
                                            )
                                            db.add(player)
                                            db.flush()
                                            total_players_saved += 1
                                        
                                        # Create player game stats
                                        stats = player_data['stats']
                                        
                                        # Check if stats already exist for this player in this game
                                        existing_stats = db.query(PlayerGameStats).filter(
                                            PlayerGameStats.game_id == game_record.id,
                                            PlayerGameStats.player_id == player.id
                                        ).first()
                                        
                                        if not existing_stats:
                                            player_stats = PlayerGameStats(
                                                game_id=game_record.id,
                                                player_id=player.id,
                                                team_id=team_record.id,
                                                goals=stats.get('goals', 0),
                                                behinds=stats.get('behinds', 0),
                                                kicks=stats.get('kicks', 0),
                                                handballs=stats.get('handballs', 0),
                                                marks=stats.get('marks', 0),
                                                tackles=stats.get('tackles', 0),
                                                hitouts=stats.get('hit_outs', 0),
                                                frees_for=stats.get('free_kicks_for', 0),
                                                frees_against=stats.get('free_kicks_against', 0),
                                                disposals=stats.get('disposals', 0),
                                                contested_possessions=stats.get('contested_possessions', 0),
                                                uncontested_possessions=stats.get('uncontested_possessions', 0),
                                                inside_50s=stats.get('inside_50s', 0),
                                                rebound_50s=stats.get('rebound_50s', 0),
                                                clearances=stats.get('clearances', 0),
                                                clangers=stats.get('clangers', 0)
                                            )
                                            db.add(player_stats)
                                            total_player_stats_saved += 1
                
                # Add a small delay to be respectful to the server
                time.sleep(0.3)
            
            season_time = time.time() - season_start_time
            print(f"  ⏱️  {season} season completed in {season_time:.2f} seconds")
            print(f"  📊 Games saved: {len(completed_games)}, Games with stats: {games_with_stats}")
            
            # Commit after each season
            db.commit()
            print(f"  💾 Committed {season} data to database")
        
        # Final commit
        db.commit()
        db.close()
        
        overall_time = time.time() - overall_start_time
        
        print(f"\n" + "=" * 60)
        print("🎉 AFL Data Collection Completed Successfully!")
        print("=" * 60)
        print(f"📅 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏱️  Total time: {overall_time:.2f} seconds ({overall_time/60:.1f} minutes)")
        print(f"\n📊 Final Summary:")
        print(f"  🏆 Teams saved: {total_teams_saved}")
        print(f"  🎮 Games saved: {total_games_saved}")
        print(f"  👥 Players saved: {total_players_saved}")
        print(f"  📈 Player stats records: {total_player_stats_saved}")
        print(f"\n✅ Database is now ready for AI analysis!")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to scrape AFL data: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("🏈 AFL Data Collection Script")
    print("This will scrape 5 years of AFL data (2020-2025) and save to database")
    print("=" * 60)
    
    # Confirm before proceeding
    response = input("Do you want to proceed with scraping 5 years of AFL data? (y/N): ")
    if response.lower() != 'y':
        print("❌ Operation cancelled by user")
        return False
    
    success = scrape_afl_data_to_database()
    
    if success:
        print("\n🎉 Data collection completed successfully!")
        print("The database now contains comprehensive AFL data for AI analysis.")
    else:
        print("\n❌ Data collection failed. Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    main() 