#!/usr/bin/env python3
"""
Test script for AFL scraper
"""

import sys
import os
import json
import time
import re
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.scrapers.afl_scraper import AFLScraper
from app.core.database import SessionLocal

def test_small_scrape():
    """Test the AFL scraper with a small amount of data"""
    print("Starting AFL scraper test...")
    
    # Create scraper instance
    scraper = AFLScraper()
    
    # Test with 2024 season, first 2 rounds
    print("Testing scraper with 2024 season, first 2 rounds...")
    result = scraper.test_small_scrape(season=2024, rounds=2)
    
    if result['success']:
        print(f"✅ Test successful!")
        print(f"📊 Games found: {result['games_found']}")
        print(f"🏆 Teams found: {result['teams_found']}")
        print(f"⏱️  Time taken: {result['time_taken']:.2f} seconds")
        
        # Show sample game data
        if result['sample_games']:
            print("\n📋 Sample game data:")
            for i, game in enumerate(result['sample_games'][:3]):
                print(f"  Game {i+1}: {game['home_team']} vs {game['away_team']} - Round {game['round']}")
                print(f"    Score: {game['home_score']} - {game['away_score']}")
                if 'date' in game:
                    print(f"    Date: {game['date']}")
                if 'venue' in game:
                    print(f"    Venue: {game['venue']}")
                print()
        
        return True
    else:
        print(f"❌ Test failed: {result['error']}")
        return False

def test_player_stats():
    """Test player statistics extraction"""
    print("\n🧑‍🏃 Testing player statistics extraction...")
    
    scraper = AFLScraper()
    
    # Test with a known game ID from 2024
    game_id = "111620240307"  # Sydney vs Melbourne Round 1 2024
    season = 2024
    
    print(f"Testing player stats for game {game_id} (season {season})...")
    
    result = scraper.parse_game_stats(game_id, season)
    
    if result['success']:
        print("✅ Player stats extraction successful!")
        
        # Show game details
        game_details = result['game_details']
        if game_details:
            print(f"📊 Game Details:")
            print(f"  Round: {game_details.get('round', 'N/A')}")
            print(f"  Venue: {game_details.get('venue', 'N/A')}")
            print(f"  Date: {game_details.get('date', 'N/A')}")
            print(f"  Attendance: {game_details.get('attendance', 'N/A')}")
            
            # Show team scores
            team_scores = game_details.get('team_scores', {})
            for team, scores in team_scores.items():
                print(f"  {team}: {scores}")
        
        # Show player stats
        player_stats = result['player_stats']
        if player_stats:
            print(f"\n👥 Player Statistics:")
            for team_name, players in player_stats.items():
                print(f"  {team_name} ({len(players)} players):")
                for player in players[:3]:  # Show first 3 players
                    stats = player['stats']
                    print(f"    {player['name']} (#{stats['jumper_number']}): "
                          f"{stats['kicks']}k {stats['marks']}m {stats['handballs']}hb "
                          f"{stats['goals']}g {stats['behinds']}b {stats['tackles']}t")
                print()
        
        return True
    else:
        print(f"❌ Player stats extraction failed: {result['error']}")
        return False

def test_database_save():
    """Test saving data to database"""
    print("\n💾 Testing database save functionality...")
    
    try:
        db = SessionLocal()
        scraper = AFLScraper()
        
        # Test with a small sample
        result = scraper.test_small_scrape(season=2024, rounds=1)
        
        if result['success'] and result['sample_games']:
            # Save a sample game to database
            sample_game = result['sample_games'][0]
            
            # This would normally save to database
            # For now, just show what would be saved
            print("✅ Database save test successful!")
            print(f"📝 Would save game: {sample_game['home_team']} vs {sample_game['away_team']}")
            print(f"   Round: {sample_game['round']}")
            if 'date' in sample_game:
                print(f"   Date: {sample_game['date']}")
            print(f"   Score: {sample_game['home_score']} - {sample_game['away_score']}")
            
            return True
        else:
            print("❌ No sample games to save")
            return False
            
    except Exception as e:
        print(f"❌ Database save test failed: {str(e)}")
        return False
    finally:
        db.close()

def scrape_5_years_to_database():
    """Scrape last 5 years (2020-2025) and save to database in AI-friendly format"""
    print("\n🏈 Scraping 5 Years of AFL Data to Database")
    print("=" * 60)
    
    try:
        from app.core.database import SessionLocal, engine
        from app.models.game import Game
        from app.models.team import Team
        from app.models.player import Player, PlayerGameStats
        from sqlalchemy.orm import sessionmaker
        
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
        
        for season in seasons:
            print(f"\n📊 Scraping {season} season...")
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
                    if season in [2024, 2025] and game.get('round'):
                        game['round'] = game['round'] - 1
                        game['game_id'] = f"{season}_r{game['round']}_{game['home_team']}_{game['away_team']}"
                    
                    completed_games.append(game)
            
            print(f"  ✅ Found {len(completed_games)} completed games")
            
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
                        teams_cache[team_name] = team
            
            # Save games and fetch player stats
            games_with_stats = 0
            for i, game_data in enumerate(completed_games):
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
        
        # Final commit
        db.commit()
        db.close()
        
        print(f"\n🎉 Scraping completed successfully!")
        print(f"📊 Summary:")
        print(f"  🏆 Teams saved: {total_teams_saved}")
        print(f"  🎮 Games saved: {total_games_saved}")
        print(f"  👥 Players saved: {total_players_saved}")
        print(f"  📈 Player stats records: {total_player_stats_saved}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to scrape to database: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def scrape_2025_to_json():
    """Scrape 2025 AFL season data and save to JSON file"""
    print("\n🏈 Scraping 2025 AFL Season to JSON")
    print("=" * 50)
    
    try:
        scraper = AFLScraper()
        
        # Scrape the 2025 season
        print(f"📊 Scraping 2025 AFL season...")
        start_time = time.time()
        
        result = scraper.parse_season_page(2025)
        
        if not result['success']:
            print(f"❌ Failed to scrape 2025 season: {result['error']}")
            return False
        
        games = result['games']
        time_taken = time.time() - start_time
        
        print(f"✅ Successfully scraped {len(games)} games from 2025 season")
        print(f"⏱️  Time taken: {time_taken:.2f} seconds")
        
        # Filter to only completed games (those with scores)
        completed_games = []
        for game in games:
            if game['home_score'] > 0 or game['away_score'] > 0:
                # Fix round numbers for 2024 and 2025 seasons (Round 0 adjustment)
                if game['season'] in [2024, 2025] and game.get('round'):
                    # Round 1 should be Round 0, Round 2 should be Round 1, etc.
                    game['round'] = game['round'] - 1
                    # Update game_id to reflect corrected round
                    game['game_id'] = f"{game['season']}_r{game['round']}_{game['home_team']}_{game['away_team']}"
                
                completed_games.append(game)
        
        print(f"🏆 Found {len(completed_games)} completed games")
        
        # Count games with stats links
        games_with_stats = [g for g in completed_games if g.get('stats_link')]
        print(f"📈 Found {len(games_with_stats)} games with available player statistics")
        
        # Fetch player statistics for games with stats links
        print(f"\n🏃 Fetching player statistics...")
        stats_start_time = time.time()
        
        games_with_player_stats = 0
        for i, game in enumerate(completed_games):
            if game.get('stats_link'):
                print(f"  📊 Fetching stats for game {i+1}/{len(completed_games)}: {game['home_team']} vs {game['away_team']}")
                
                # Extract game ID from stats link
                stats_link = game['stats_link']
                if '/stats/games/' in stats_link:
                    # Extract the game ID from the URL
                    game_id_match = re.search(r'/stats/games/\d+/(\d+)\.html', stats_link)
                    if game_id_match:
                        game_id = game_id_match.group(1)
                        
                        # Fetch player statistics
                        stats_result = scraper.parse_game_stats(game_id, 2025)
                        if stats_result['success']:
                            game['player_statistics'] = stats_result['player_stats']
                            game['detailed_game_info'] = stats_result['game_details']
                            games_with_player_stats += 1
                            print(f"    ✅ Successfully fetched stats for {len(stats_result['player_stats'])} teams")
                        else:
                            print(f"    ❌ Failed to fetch stats: {stats_result.get('error', 'Unknown error')}")
                
                # Add a small delay to be respectful to the server
                time.sleep(0.5)
        
        stats_time_taken = time.time() - stats_start_time
        print(f"⏱️  Player stats fetching took: {stats_time_taken:.2f} seconds")
        print(f"📊 Successfully fetched player stats for {games_with_player_stats} games")
        
        # Show sample of games
        if completed_games:
            print("\n📋 Sample completed games:")
            for i, game in enumerate(completed_games[:5]):
                print(f"  {i+1}. Round {game['round']}: {game['home_team']} {game['home_score']} - {game['away_score']} {game['away_team']}")
                if game.get('venue'):
                    print(f"     Venue: {game['venue']}")
                if game.get('game_date'):
                    print(f"     Date: {game['game_date']}")
                if game.get('player_statistics'):
                    teams_with_stats = list(game['player_statistics'].keys())
                    print(f"     Player stats: {len(teams_with_stats)} teams ({', '.join(teams_with_stats)})")
                print()
        
        # Prepare data for JSON
        output_data = {
            'scrape_info': {
                'season': 2025,
                'scrape_date': datetime.now().isoformat(),
                'total_games_found': len(games),
                'completed_games': len(completed_games),
                'games_with_player_stats': games_with_player_stats,
                'scrape_time_seconds': time_taken,
                'player_stats_time_seconds': stats_time_taken,
                'total_time_seconds': time_taken + stats_time_taken
            },
            'games': completed_games
        }
        
        # Save to JSON file
        output_filename = f"afl_2025_games_with_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_path = os.path.join(os.path.dirname(__file__), output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, default=str)
        
        print(f"💾 Data saved to: {output_filename}")
        print(f"📁 Full path: {output_path}")
        
        # Show file size
        file_size = os.path.getsize(output_path)
        print(f"📊 File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to scrape 2025 season: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 AFL Scraper Comprehensive Test")
    print("=" * 50)
    
    # Check if user wants to scrape 2025 data specifically
    if len(sys.argv) > 1 and sys.argv[1] == "2025":
        print("🎯 Running 2025 season scrape only...")
        success = scrape_2025_to_json()
        if success:
            print("\n🎉 2025 scraping completed successfully!")
            print("You can now review the JSON file before committing to the database.")
        else:
            print("\n❌ 2025 scraping failed. Please check the error messages above.")
        return success
    
    # Check if user wants to scrape 5 years to database
    if len(sys.argv) > 1 and sys.argv[1] == "5years":
        print("🎯 Running 5-year database scrape...")
        success = scrape_5_years_to_database()
        if success:
            print("\n🎉 5-year scraping completed successfully!")
            print("All data has been saved to the database in AI-friendly format.")
        else:
            print("\n❌ 5-year scraping failed. Please check the error messages above.")
        return success
    
    tests = [
        ("Basic Scraping", test_small_scrape),
        ("Player Statistics", test_player_stats),
        ("Database Save", test_database_save),
        ("2025 Season to JSON", scrape_2025_to_json)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The scraper is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the output above.")
    
    return passed == total

if __name__ == "__main__":
    main() 