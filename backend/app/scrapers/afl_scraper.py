import requests
from bs4 import BeautifulSoup
import time
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.game import Game
from app.models.team import Team
from app.models.player import Player, PlayerGameStats
import logging

logger = logging.getLogger(__name__)

class AFLScraper:
    def __init__(self):
        self.base_url = "https://afltables.com/afl"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def test_small_scrape(self, season: int = 2024, rounds: int = 2) -> Dict:
        """Test the scraper with a small amount of data"""
        import time
        start_time = time.time()
        
        try:
            print(f"🧪 Testing AFL scraper for {season} season, first {rounds} rounds...")
            
            # Parse the season page
            season_data = self.parse_season_page(season)
            
            if not season_data['success']:
                return {
                    'success': False,
                    'error': season_data['error']
                }
            
            games = season_data['games']
            
            # Filter to first N rounds
            round_games = []
            current_round = 0
            for game in games:
                if game['round'] > rounds:
                    break
                round_games.append(game)
            
            # Get unique teams
            teams = set()
            for game in round_games:
                teams.add(game['home_team'])
                teams.add(game['away_team'])
            
            # Get sample games for testing
            sample_games = round_games[:5] if len(round_games) > 5 else round_games
            
            time_taken = time.time() - start_time
            
            return {
                'success': True,
                'games_found': len(round_games),
                'teams_found': len(teams),
                'time_taken': time_taken,
                'sample_games': sample_games,
                'all_games': round_games
            }
            
        except Exception as e:
            logger.error(f"Error in test_small_scrape: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_season_data(self, season: int) -> Optional[Dict]:
        """Get season overview data"""
        try:
            url = f"{self.base_url}/seas/{season}.html"
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all tables
            tables = soup.find_all('table')
            
            # Look for the ladder table (usually the first table)
            ladder_data = []
            if tables:
                ladder_table = tables[0]
                rows = ladder_table.find_all('tr')[1:]  # Skip header
                
                for row in rows:
                    cols = row.find_all(['td', 'th'])
                    if len(cols) >= 4:
                        team_name = cols[1].get_text(strip=True)
                        ladder_data.append({
                            'position': cols[0].get_text(strip=True),
                            'team': team_name,
                            'played': cols[2].get_text(strip=True),
                            'points': cols[3].get_text(strip=True)
                        })
            
            # Look for round links
            round_links = []
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                if f'seas/{season}/' in href and 'round' in href.lower():
                    round_links.append(href)
            
            return {
                'season': season,
                'ladder': ladder_data,
                'rounds': round_links
            }
            
        except Exception as e:
            logger.error(f"Error getting season data: {str(e)}")
            return None
    
    def _get_round_data(self, season: int, round_num: int) -> Optional[Dict]:
        """Get data for a specific round"""
        try:
            # Try different URL patterns
            url_patterns = [
                f"{self.base_url}/seas/{season}/round{round_num}.html",
                f"{self.base_url}/seas/{season}/r{round_num}.html",
                f"{self.base_url}/seas/{season}/round_{round_num}.html"
            ]
            
            round_data = None
            for url in url_patterns:
                try:
                    response = self.session.get(url)
                    if response.status_code == 200:
                        round_data = self._parse_round_page(response.content, season, round_num)
                        break
                except:
                    continue
            
            return round_data
            
        except Exception as e:
            logger.error(f"Error getting round {round_num} data: {str(e)}")
            return None
    
    def _parse_round_page(self, content: bytes, season: int, round_num: int) -> Optional[Dict]:
        """Parse a round page to extract game data"""
        try:
            soup = BeautifulSoup(content, 'html.parser')
            
            # Look for game tables
            tables = soup.find_all('table')
            games = []
            
            for table in tables:
                # Look for tables that might contain game data
                rows = table.find_all('tr')
                
                for row in rows:
                    cols = row.find_all(['td', 'th'])
                    if len(cols) >= 6:  # Minimum columns for a game
                        # Check if this looks like a game row
                        first_col = cols[0].get_text(strip=True)
                        
                        # Look for date patterns or team names
                        if (re.match(r'\d{1,2}/\d{1,2}/\d{4}', first_col) or 
                            any(team_name in str(cols) for team_name in ['Carlton', 'Collingwood', 'Essendon', 'Richmond', 'Geelong', 'Hawthorn', 'Melbourne', 'North Melbourne', 'St Kilda', 'Sydney', 'Western Bulldogs', 'Adelaide', 'Brisbane', 'Fremantle', 'Gold Coast', 'GWS', 'Port Adelaide', 'West Coast'])):
                            
                            game_data = self._extract_game_from_row(cols, season, round_num)
                            if game_data:
                                games.append(game_data)
            
            return {
                'round': round_num,
                'season': season,
                'games': games
            }
            
        except Exception as e:
            logger.error(f"Error parsing round page: {str(e)}")
            return None
    
    def _extract_game_from_row(self, cols, season: int, round_num: int) -> Optional[Dict]:
        """Extract game data from a table row"""
        try:
            # This is a simplified extraction - we'll need to adapt based on actual structure
            if len(cols) < 6:
                return None
            
            # Try to identify teams and scores
            text_content = ' '.join([col.get_text(strip=True) for col in cols])
            
            # Look for team names
            teams = ['Carlton', 'Collingwood', 'Essendon', 'Richmond', 'Geelong', 'Hawthorn', 
                    'Melbourne', 'North Melbourne', 'St Kilda', 'Sydney', 'Western Bulldogs', 
                    'Adelaide', 'Brisbane', 'Fremantle', 'Gold Coast', 'GWS', 'Port Adelaide', 'West Coast']
            
            found_teams = []
            for team in teams:
                if team in text_content:
                    found_teams.append(team)
            
            if len(found_teams) >= 2:
                # Look for scores (numbers that could be scores)
                scores = []
                for col in cols:
                    text = col.get_text(strip=True)
                    if re.match(r'^\d+$', text) and len(text) <= 3:
                        scores.append(int(text))
                
                if len(scores) >= 2:
                    return {
                        'home_team': found_teams[0],
                        'away_team': found_teams[1],
                        'home_score': scores[0],
                        'away_score': scores[1],
                        'season': season,
                        'round': round_num,
                        'game_id': f"{season}_r{round_num}_{found_teams[0]}_{found_teams[1]}"
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting game from row: {str(e)}")
            return None
    
    def _get_game_player_stats(self, game_id: str) -> List[Dict]:
        """Get player statistics for a specific game"""
        try:
            # This would need to be implemented based on the actual game page structure
            # For now, return empty list
            return []
            
        except Exception as e:
            logger.error(f"Error getting player stats for game {game_id}: {str(e)}")
            return []
    
    def scrape_full_history(self, start_year: int = 2019, end_year: int = 2024) -> Dict:
        """Scrape full historical data for the specified years"""
        results = {
            "success": True,
            "years_processed": 0,
            "total_games": 0,
            "total_teams": 0,
            "total_players": 0,
            "errors": []
        }
        
        for year in range(start_year, end_year + 1):
            try:
                print(f"📅 Processing year {year}...")
                year_result = self._scrape_year(year)
                
                if year_result['success']:
                    results["years_processed"] += 1
                    results["total_games"] += year_result.get('games', 0)
                    results["total_teams"] += year_result.get('teams', 0)
                    results["total_players"] += year_result.get('players', 0)
                else:
                    results["errors"].append(f"Year {year}: {year_result.get('error', 'Unknown error')}")
                
                time.sleep(2)  # Be respectful to the server
                
            except Exception as e:
                results["errors"].append(f"Year {year}: {str(e)}")
        
        return results
    
    def _scrape_year(self, year: int) -> Dict:
        """Scrape a single year of data"""
        try:
            season_data = self._get_season_data(year)
            if not season_data:
                return {"success": False, "error": "Could not get season data"}
            
            games = []
            teams = set()
            players = 0
            
            # Process all rounds
            for round_num in range(1, 25):  # Assume max 24 rounds
                round_data = self._get_round_data(year, round_num)
                
                if round_data and round_data['games']:
                    games.extend(round_data['games'])
                    
                    for game in round_data['games']:
                        teams.add(game['home_team'])
                        teams.add(game['away_team'])
                        
                        # Get player stats
                        if game.get('game_id'):
                            player_stats = self._get_game_player_stats(game['game_id'])
                            players += len(player_stats)
                
                time.sleep(1)
            
            return {
                "success": True,
                "games": len(games),
                "teams": len(teams),
                "players": players,
                "year": year
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_game_links_for_round(self, season: int, round_num: int) -> list:
        """Get all game links for a given round from the round page."""
        url_patterns = [
            f"{self.base_url}/seas/{season}/round{round_num}.html",
            f"{self.base_url}/seas/{season}/r{round_num}.html",
            f"{self.base_url}/seas/{season}/round_{round_num}.html"
        ]
        for url in url_patterns:
            try:
                response = self.session.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    game_links = []
                    for a in soup.find_all('a', href=True):
                        href = a['href']
                        if href.startswith('games/') and href.endswith('.html'):
                            game_links.append("https://afltables.com/afl/" + href)
                    return game_links
            except Exception:
                continue
        return []

    def parse_player_stats_from_game(self, game_url: str) -> list:
        """Parse player stats from a single game page."""
        try:
            response = self.session.get(game_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')
            player_stats = []
            for table in tables:
                headers = [th.get_text(strip=True) for th in table.find_all('th')]
                if 'Player' in headers:
                    for row in table.find_all('tr')[1:]:
                        cells = row.find_all('td')
                        if not cells or len(cells) < 2:
                            continue
                        stat = dict(zip(headers, [cell.get_text(strip=True) for cell in cells]))
                        player_stats.append(stat)
            return player_stats
        except Exception as e:
            logger.error(f"Error parsing player stats from {game_url}: {e}")
            return []

    def scrape_and_save_round(self, db: Session, season: int, round_num: int):
        """Scrape all games and player stats for a round and save to DB."""
        print(f"Scraping season {season} round {round_num}...")
        game_links = self.get_game_links_for_round(season, round_num)
        print(f"Found {len(game_links)} game links.")
        for game_url in game_links:
            print(f"Processing game: {game_url}")
            player_stats = self.parse_player_stats_from_game(game_url)
            print(f"  Found {len(player_stats)} player stats.")
            # Here you would call your save logic, e.g. self.save_player_stats_to_db(db, player_stats, game_url)
            # For now, just print a sample
            if player_stats:
                print(f"  Sample player: {player_stats[0]}")

    def parse_season_page(self, season: int) -> Dict:
        """Parse the main season page to extract all games"""
        try:
            url = f"{self.base_url}/seas/{season}.html"
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            games = []
            current_round = None
            processed_tables = set()  # Track processed tables to avoid duplicates
            
            # Find all tables
            tables = soup.find_all('table')
            
            for table in tables:
                rows = table.find_all('tr')
                if len(rows) < 1:
                    continue
                
                # Check if this is a round header table
                first_row = rows[0]
                if 'Round' in first_row.get_text():
                    round_match = re.search(r'Round (\d+)', first_row.get_text())
                    if round_match:
                        current_round = int(round_match.group(1))
                        continue
                
                # Check if this table contains game data by looking for team links
                team_links = table.find_all('a', href=lambda x: x and 'teams/' in x)
                if len(team_links) >= 2 and id(table) not in processed_tables:
                    # This looks like a game table
                    processed_tables.add(id(table))
                    # Games are stored in pairs of rows (home team, away team)
                    for i in range(0, len(rows), 2):
                        if i + 1 < len(rows):
                            home_row = rows[i]
                            away_row = rows[i + 1]
                            
                            game_data = self._parse_game_rows(home_row, away_row, season, current_round)
                            if game_data:
                                games.append(game_data)
            
            # Remove duplicates based on game_id
            unique_games = {}
            for game in games:
                game_id = game.get('game_id', '')
                if game_id and game_id not in unique_games:
                    unique_games[game_id] = game
            
            return {
                "success": True,
                "games": list(unique_games.values()),
                "season": season
            }
            
        except Exception as e:
            logger.error(f"Error parsing season page: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _parse_game_rows(self, home_row, away_row, season: int, round_num: int = None) -> Optional[Dict]:
        """Parse two rows representing a game (home and away teams)"""
        try:
            home_cells = home_row.find_all(['td', 'th'])
            away_cells = away_row.find_all(['td', 'th'])
            
            if len(home_cells) < 4 or len(away_cells) < 4:
                return None
            
            # Extract team names from links
            home_team_link = home_cells[0].find('a', href=lambda x: x and 'teams/' in x)
            away_team_link = away_cells[0].find('a', href=lambda x: x and 'teams/' in x)
            
            if not home_team_link or not away_team_link:
                return None
            
            home_team = home_team_link.get_text(strip=True)
            away_team = away_team_link.get_text(strip=True)
            
            # Skip if same team (this shouldn't happen in real games)
            if home_team == away_team:
                return None
            
            # Extract scores (third column)
            home_score_text = home_cells[2].get_text(strip=True)
            away_score_text = away_cells[2].get_text(strip=True)
            
            home_score = int(home_score_text) if home_score_text.isdigit() else 0
            away_score = int(away_score_text) if away_score_text.isdigit() else 0
            
            # Extract game details from the last cell
            game_details = away_cells[-1].get_text(strip=True)
            
            # Extract venue and date if available
            venue = None
            game_date = None
            
            # Look for venue pattern
            venue_match = re.search(r'Venue:\s*([^(]+)', game_details)
            if venue_match:
                venue = venue_match.group(1).strip()
            
            # Look for date pattern
            date_match = re.search(r'(\w{3}\s+\d{1,2}-\w{3}-\d{4})', game_details)
            if date_match:
                try:
                    date_str = date_match.group(1)
                    game_date = datetime.strptime(date_str, '%a %d-%b-%Y')
                except:
                    pass
            
            # Extract match stats link
            stats_link = None
            stats_a = away_cells[-1].find('a', href=True)
            if stats_a and 'stats/games' in stats_a['href']:
                # Fix the stats link path
                href = stats_a['href']
                if href.startswith('../'):
                    href = href[3:]  # Remove ../
                stats_link = f"{self.base_url}/{href}"
                
                # Extract round number from stats link if not already set
                if not round_num:
                    round_match = re.search(r'/(\d{1,2})/', href)
                    if round_match:
                        round_num = int(round_match.group(1))
            
            # If we still don't have a round number, try to infer from context
            if not round_num:
                # Look for round info in the game details
                round_match = re.search(r'Round (\d+)', game_details)
                if round_match:
                    round_num = int(round_match.group(1))
            
            return {
                'home_team': home_team,
                'away_team': away_team,
                'home_score': home_score,
                'away_score': away_score,
                'season': season,
                'round': round_num,
                'venue': venue,
                'game_date': game_date,
                'stats_link': stats_link,
                'game_id': f"{season}_r{round_num}_{home_team}_{away_team}" if round_num else f"{season}_{home_team}_{away_team}"
            }
            
        except Exception as e:
            logger.error(f"Error parsing game rows: {str(e)}")
            return None
    
    def parse_game_stats(self, game_id: str, season: int) -> Dict:
        """Parse detailed game statistics including player stats"""
        try:
            url = f"{self.base_url}/stats/games/{season}/{game_id}.html"
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract game details
            game_details = self._extract_game_details(soup)
            
            # Extract player statistics
            player_stats = self._extract_player_stats(soup)
            
            return {
                'success': True,
                'game_details': game_details,
                'player_stats': player_stats
            }
            
        except Exception as e:
            logger.error(f"Error parsing game stats for {game_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _extract_game_details(self, soup: BeautifulSoup) -> Dict:
        """Extract game details from the stats page"""
        try:
            # Find the main game table
            game_table = soup.find('table', style=lambda x: x and 'font: 12px Verdana' in x)
            if not game_table:
                return {}
            
            rows = game_table.find_all('tr')
            if len(rows) < 3:
                return {}
            
            # Extract round, venue, date, attendance
            details = {}
            
            # Round info is in the first row
            first_row = rows[0]
            round_text = first_row.get_text()
            if 'Round:' in round_text:
                round_match = re.search(r'Round:\s*(\d+)', round_text)
                if round_match:
                    details['round'] = int(round_match.group(1))
            
            # Venue
            venue_link = first_row.find('a', href=lambda x: x and 'venues' in x)
            if venue_link:
                details['venue'] = venue_link.get_text().strip()
            
            # Date
            date_match = re.search(r'Date:\s*([^,]+,\s*\d+-\w+-\d+\s+\d+:\d+\s+\w+)', round_text)
            if date_match:
                details['date'] = date_match.group(1).strip()
            
            # Attendance
            attendance_match = re.search(r'Attendance:\s*(\d+)', round_text)
            if attendance_match:
                details['attendance'] = int(attendance_match.group(1))
            
            # Team scores
            team_scores = {}
            for i in range(1, 3):  # First two team rows
                if i < len(rows):
                    team_row = rows[i]
                    team_link = team_row.find('a', href=lambda x: x and 'teams' in x)
                    if team_link:
                        team_name = team_link.get_text().strip()
                        scores = []
                        score_cells = team_row.find_all('td')[1:5]  # Skip team name cell
                        for cell in score_cells:
                            score_text = cell.get_text().strip()
                            if score_text:
                                # Parse AFL score format (goals.behinds.total)
                                score_parts = score_text.split('.')
                                if len(score_parts) >= 3:
                                    goals = int(score_parts[0])
                                    behinds = int(score_parts[1])
                                    total = int(score_parts[2])
                                    scores.append({
                                        'goals': goals,
                                        'behinds': behinds,
                                        'total': total,
                                        'raw': score_text
                                    })
                                else:
                                    # Fallback to just the number
                                    scores.append({
                                        'total': int(score_text),
                                        'raw': score_text
                                    })
                        team_scores[team_name] = scores
            
            details['team_scores'] = team_scores
            
            return details
            
        except Exception as e:
            logger.error(f"Error extracting game details: {str(e)}")
            return {}
    
    def _extract_player_stats(self, soup: BeautifulSoup) -> Dict:
        """Extract player statistics from the stats page"""
        try:
            player_stats = {}
            
            # Find all player stat tables
            stat_tables = soup.find_all('table', class_='sortable')
            
            for table in stat_tables:
                # Check if this is a player stats table
                header = table.find('th')
                if not header or 'Match Statistics' not in header.get_text():
                    continue
                
                # Extract team name from header
                team_name = header.get_text().split('Match Statistics')[0].strip()
                
                # Parse player rows
                tbody = table.find('tbody')
                if not tbody:
                    continue
                
                players = []
                rows = tbody.find_all('tr')
                
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) < 15:  # Need minimum columns for stats
                        continue
                    
                    # Extract player info
                    player_link = cells[1].find('a')
                    if not player_link:
                        continue
                    
                    player_name = player_link.get_text().strip()
                    jumper_number = cells[0].get_text().strip()
                    
                    # Extract statistics
                    stats = {
                        'jumper_number': jumper_number,
                        'kicks': self._parse_stat(cells[2]),
                        'marks': self._parse_stat(cells[3]),
                        'handballs': self._parse_stat(cells[4]),
                        'disposals': self._parse_stat(cells[5]),
                        'goals': self._parse_stat(cells[6]),
                        'behinds': self._parse_stat(cells[7]),
                        'hit_outs': self._parse_stat(cells[8]),
                        'tackles': self._parse_stat(cells[9]),
                        'rebound_50s': self._parse_stat(cells[10]),
                        'inside_50s': self._parse_stat(cells[11]),
                        'clearances': self._parse_stat(cells[12]),
                        'clangers': self._parse_stat(cells[13]),
                        'free_kicks_for': self._parse_stat(cells[14]),
                        'free_kicks_against': self._parse_stat(cells[15]),
                        'brownlow_votes': self._parse_stat(cells[16]) if len(cells) > 16 else 0,
                        'contested_possessions': self._parse_stat(cells[17]) if len(cells) > 17 else 0,
                        'uncontested_possessions': self._parse_stat(cells[18]) if len(cells) > 18 else 0,
                        'contested_marks': self._parse_stat(cells[19]) if len(cells) > 19 else 0,
                        'marks_inside_50': self._parse_stat(cells[20]) if len(cells) > 20 else 0,
                        'one_percenters': self._parse_stat(cells[21]) if len(cells) > 21 else 0,
                        'bounces': self._parse_stat(cells[22]) if len(cells) > 22 else 0,
                        'goal_assists': self._parse_stat(cells[23]) if len(cells) > 23 else 0,
                        'percentage_played': self._parse_stat(cells[24]) if len(cells) > 24 else 100
                    }
                    
                    players.append({
                        'name': player_name,
                        'stats': stats
                    })
                
                player_stats[team_name] = players
            
            return player_stats
            
        except Exception as e:
            logger.error(f"Error extracting player stats: {str(e)}")
            return {}
    
    def _parse_stat(self, cell) -> int:
        """Parse a statistic cell and return integer value"""
        try:
            text = cell.get_text().strip()
            if text and text != '&nbsp;':
                return int(text)
            return 0
        except (ValueError, AttributeError):
            return 0 

    def scrape_multiple_seasons(self, start_year: int = 2019, end_year: int = 2024, save_to_db: bool = True) -> Dict:
        """
        Scrape multiple seasons of AFL data and save to database
        
        Args:
            start_year: Starting year (inclusive)
            end_year: Ending year (inclusive)
            save_to_db: Whether to save data to database
            
        Returns:
            Dictionary with scraping results
        """
        import time
        start_time = time.time()
        
        results = {
            'success': True,
            'seasons_processed': 0,
            'total_games': 0,
            'total_players': 0,
            'total_player_stats': 0,
            'errors': [],
            'time_taken': 0,
            'season_details': []
        }
        
        try:
            print(f"🚀 Starting comprehensive AFL scraping for {start_year}-{end_year}...")
            
            for year in range(start_year, end_year + 1):
                print(f"\n📊 Processing {year} season...")
                season_start = time.time()
                
                season_result = self._scrape_season(year, save_to_db)
                
                if season_result['success']:
                    results['seasons_processed'] += 1
                    results['total_games'] += season_result['games_found']
                    results['total_players'] += season_result['players_found']
                    results['total_player_stats'] += season_result['player_stats_found']
                    
                    results['season_details'].append({
                        'year': year,
                        'games': season_result['games_found'],
                        'players': season_result['players_found'],
                        'player_stats': season_result['player_stats_found'],
                        'time_taken': season_result['time_taken']
                    })
                    
                    print(f"✅ {year}: {season_result['games_found']} games, "
                          f"{season_result['players_found']} players, "
                          f"{season_result['player_stats_found']} player stats "
                          f"({season_result['time_taken']:.1f}s)")
                else:
                    results['errors'].append({
                        'year': year,
                        'error': season_result['error']
                    })
                    print(f"❌ {year}: {season_result['error']}")
                
                # Be respectful to the server
                time.sleep(2)
            
            results['time_taken'] = time.time() - start_time
            
            print(f"\n🎯 Scraping complete!")
            print(f"📊 Seasons processed: {results['seasons_processed']}")
            print(f"🎮 Total games: {results['total_games']}")
            print(f"👥 Total players: {results['total_players']}")
            print(f"📈 Total player stats: {results['total_player_stats']}")
            print(f"⏱️  Total time: {results['time_taken']:.1f} seconds")
            
            if results['errors']:
                print(f"⚠️  Errors: {len(results['errors'])}")
                for error in results['errors']:
                    print(f"   {error['year']}: {error['error']}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error in comprehensive scraping: {str(e)}")
            results['success'] = False
            results['errors'].append({
                'year': 'general',
                'error': str(e)
            })
            return results
    
    def _scrape_season(self, year: int, save_to_db: bool = True) -> Dict:
        """Scrape a single season and optionally save to database"""
        import time
        start_time = time.time()
        
        try:
            # Parse season page
            season_data = self.parse_season_page(year)
            
            if not season_data['success']:
                return {
                    'success': False,
                    'error': season_data['error']
                }
            
            games = season_data['games']
            games_found = len(games)
            players_found = 0
            player_stats_found = 0
            
            # Save games to database if requested
            if save_to_db:
                db = SessionLocal()
                try:
                    for game in games:
                        # Save or update game
                        game_record = self._save_game_to_db(db, game, year)
                        
                        # Get player stats for this game if available
                        if game.get('game_id'):
                            stats_result = self.parse_game_stats(game['game_id'], year)
                            if stats_result['success']:
                                players_found += self._save_player_stats_to_db(db, stats_result, game_record)
                                player_stats_found += self._count_player_stats(stats_result)
                        
                        # Be respectful to the server
                        time.sleep(0.5)
                    
                    db.commit()
                except Exception as e:
                    db.rollback()
                    logger.error(f"Database error for {year}: {str(e)}")
                    return {
                        'success': False,
                        'error': f"Database error: {str(e)}"
                    }
                finally:
                    db.close()
            
            time_taken = time.time() - start_time
            
            return {
                'success': True,
                'games_found': games_found,
                'players_found': players_found,
                'player_stats_found': player_stats_found,
                'time_taken': time_taken
            }
            
        except Exception as e:
            logger.error(f"Error scraping {year} season: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _save_game_to_db(self, db: Session, game_data: Dict, year: int) -> Game:
        """Save or update a game in the database"""
        try:
            # Check if game already exists
            existing_game = db.query(Game).filter(
                Game.home_team == game_data['home_team'],
                Game.away_team == game_data['away_team'],
                Game.round == game_data['round'],
                Game.season == year
            ).first()
            
            if existing_game:
                # Update existing game
                existing_game.home_score = game_data['home_score']
                existing_game.away_score = game_data['away_score']
                if 'venue' in game_data:
                    existing_game.venue = game_data['venue']
                if 'date' in game_data:
                    existing_game.date = game_data['date']
                return existing_game
            else:
                # Create new game
                new_game = Game(
                    season=year,
                    round=game_data['round'],
                    home_team=game_data['home_team'],
                    away_team=game_data['away_team'],
                    home_score=game_data['home_score'],
                    away_score=game_data['away_score'],
                    venue=game_data.get('venue'),
                    date=game_data.get('date'),
                    game_id=game_data.get('game_id')
                )
                db.add(new_game)
                db.flush()  # Get the ID
                return new_game
                
        except Exception as e:
            logger.error(f"Error saving game to database: {str(e)}")
            raise
    
    def _save_player_stats_to_db(self, db: Session, stats_result: Dict, game_record: Game) -> int:
        """Save player statistics to database"""
        try:
            players_saved = 0
            player_stats = stats_result.get('player_stats', {})
            
            for team_name, players in player_stats.items():
                for player_data in players:
                    # Get or create player
                    player = self._get_or_create_player(db, player_data['name'])
                    
                    # Save player game stats
                    stats = player_data['stats']
                    game_stats = PlayerGameStats(
                        player_id=player.id,
                        game_id=game_record.id,
                        team=team_name,
                        jumper_number=stats.get('jumper_number'),
                        kicks=stats.get('kicks', 0),
                        marks=stats.get('marks', 0),
                        handballs=stats.get('handballs', 0),
                        disposals=stats.get('disposals', 0),
                        goals=stats.get('goals', 0),
                        behinds=stats.get('behinds', 0),
                        hit_outs=stats.get('hit_outs', 0),
                        tackles=stats.get('tackles', 0),
                        rebound_50s=stats.get('rebound_50s', 0),
                        inside_50s=stats.get('inside_50s', 0),
                        clearances=stats.get('clearances', 0),
                        clangers=stats.get('clangers', 0),
                        free_kicks_for=stats.get('free_kicks_for', 0),
                        free_kicks_against=stats.get('free_kicks_against', 0),
                        brownlow_votes=stats.get('brownlow_votes', 0),
                        contested_possessions=stats.get('contested_possessions', 0),
                        uncontested_possessions=stats.get('uncontested_possessions', 0),
                        contested_marks=stats.get('contested_marks', 0),
                        marks_inside_50=stats.get('marks_inside_50', 0),
                        one_percenters=stats.get('one_percenters', 0),
                        bounces=stats.get('bounces', 0),
                        goal_assists=stats.get('goal_assists', 0),
                        percentage_played=stats.get('percentage_played', 100)
                    )
                    
                    db.add(game_stats)
                    players_saved += 1
            
            return players_saved
            
        except Exception as e:
            logger.error(f"Error saving player stats to database: {str(e)}")
            raise
    
    def _get_or_create_player(self, db: Session, player_name: str) -> Player:
        """Get existing player or create new one"""
        try:
            player = db.query(Player).filter(Player.name == player_name).first()
            if not player:
                player = Player(name=player_name)
                db.add(player)
                db.flush()  # Get the ID
            return player
        except Exception as e:
            logger.error(f"Error getting/creating player: {str(e)}")
            raise
    
    def _count_player_stats(self, stats_result: Dict) -> int:
        """Count total number of player statistics"""
        try:
            count = 0
            player_stats = stats_result.get('player_stats', {})
            for team_players in player_stats.values():
                count += len(team_players)
            return count
        except Exception as e:
            logger.error(f"Error counting player stats: {str(e)}")
            return 0 