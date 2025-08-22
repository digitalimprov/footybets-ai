import requests
from bs4 import BeautifulSoup
import time
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.game import Game
from app.models.team import Team
import logging

logger = logging.getLogger(__name__)

class AFLTablesUpcomingScraper:
    """Specialized scraper for upcoming AFL games from afltables.com"""
    
    def __init__(self):
        self.base_url = "https://afltables.com/afl"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_upcoming_games(self, weeks_ahead: int = 2) -> Dict:
        """
        Get upcoming AFL games for the next specified weeks
        
        Args:
            weeks_ahead: How many weeks ahead to look for games
            
        Returns:
            Dictionary with upcoming games data
        """
        try:
            current_year = datetime.now().year
            current_date = datetime.now()
            end_date = current_date + timedelta(weeks=weeks_ahead)
            
            logger.info(f"Scraping upcoming AFL games from {current_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            
            # Get current season's fixture
            season_data = self._get_season_fixture(current_year)
            
            if not season_data['success']:
                return season_data
            
            # Filter for upcoming games only
            upcoming_games = []
            for game in season_data['games']:
                game_date = game.get('game_date')
                if game_date and current_date <= game_date <= end_date:
                    upcoming_games.append(game)
            
            return {
                'success': True,
                'games': upcoming_games,
                'total_games': len(upcoming_games),
                'date_range': {
                    'start': current_date.strftime('%Y-%m-%d'),
                    'end': end_date.strftime('%Y-%m-%d')
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting upcoming games: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_season_fixture(self, season: int) -> Dict:
        """Get the complete season fixture from afltables.com"""
        try:
            url = f"{self.base_url}/seas/{season}.html"
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            games = []
            current_round = None
            
            # Find all tables that might contain game data
            tables = soup.find_all('table')
            
            for table in tables:
                rows = table.find_all('tr')
                
                # Look for round headers
                for row in rows:
                    if 'Round' in row.get_text() and re.search(r'Round (\d+)', row.get_text()):
                        round_match = re.search(r'Round (\d+)', row.get_text())
                        if round_match:
                            current_round = int(round_match.group(1))
                            continue
                
                # Look for game data in tables with team links
                team_links = table.find_all('a', href=lambda x: x and 'teams/' in x)
                if len(team_links) >= 2:
                    # Parse games from this table
                    table_games = self._parse_fixture_table(table, season, current_round)
                    games.extend(table_games)
            
            # Remove duplicates and sort by date
            unique_games = self._deduplicate_games(games)
            unique_games.sort(key=lambda x: x.get('game_date', datetime.min))
            
            return {
                'success': True,
                'games': unique_games,
                'season': season
            }
            
        except Exception as e:
            logger.error(f"Error getting season fixture: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _parse_fixture_table(self, table, season: int, current_round: int = None) -> List[Dict]:
        """Parse a fixture table to extract game data"""
        games = []
        rows = table.find_all('tr')
        
        i = 0
        while i < len(rows):
            row = rows[i]
            
            # Check if this row contains team information
            team_link = row.find('a', href=lambda x: x and 'teams/' in x)
            if not team_link:
                i += 1
                continue
            
            # This might be the start of a game (home team)
            home_team = team_link.get_text(strip=True)
            
            # Look for the away team in the next row
            if i + 1 < len(rows):
                away_row = rows[i + 1]
                away_team_link = away_row.find('a', href=lambda x: x and 'teams/' in x)
                
                if away_team_link:
                    away_team = away_team_link.get_text(strip=True)
                    
                    # Extract game details
                    game_data = self._extract_game_details(row, away_row, season, current_round)
                    if game_data:
                        game_data['home_team'] = home_team
                        game_data['away_team'] = away_team
                        games.append(game_data)
                    
                    i += 2  # Skip both rows
                    continue
            
            i += 1
        
        return games
    
    def _extract_game_details(self, home_row, away_row, season: int, round_num: int = None) -> Optional[Dict]:
        """Extract game details from home and away team rows"""
        try:
            # Extract date and time information
            game_date = None
            venue = None
            
            # Look for date information in either row
            for row in [home_row, away_row]:
                cells = row.find_all(['td', 'th'])
                for cell in cells:
                    cell_text = cell.get_text(strip=True)
                    
                    # Look for date patterns
                    date_match = re.search(r'(\w{3}\s+\d{1,2}-\w{3}-\d{4})', cell_text)
                    if date_match and not game_date:
                        try:
                            date_str = date_match.group(1)
                            game_date = datetime.strptime(date_str, '%a %d-%b-%Y')
                        except:
                            pass
                    
                    # Look for time patterns
                    time_match = re.search(r'(\d{1,2}:\d{2}\s*[ap]m)', cell_text, re.IGNORECASE)
                    if time_match and game_date:
                        try:
                            time_str = time_match.group(1)
                            time_obj = datetime.strptime(time_str, '%I:%M %p').time()
                            game_date = datetime.combine(game_date.date(), time_obj)
                        except:
                            pass
                    
                    # Look for venue information
                    if 'Venue:' in cell_text or any(venue_name in cell_text for venue_name in ['MCG', 'SCG', 'Optus Stadium', 'Marvel Stadium']):
                        venue_match = re.search(r'Venue:\s*([^(]+)', cell_text)
                        if venue_match:
                            venue = venue_match.group(1).strip()
                        else:
                            # Try to extract known venue names
                            known_venues = ['MCG', 'SCG', 'Optus Stadium', 'Marvel Stadium', 'Adelaide Oval', 'Gabba', 'GMHBA Stadium']
                            for known_venue in known_venues:
                                if known_venue in cell_text:
                                    venue = known_venue
                                    break
            
            # Extract round number if not provided
            if not round_num:
                for row in [home_row, away_row]:
                    round_match = re.search(r'Round (\d+)', row.get_text())
                    if round_match:
                        round_num = int(round_match.group(1))
                        break
            
            return {
                'season': season,
                'round': round_num,
                'game_date': game_date,
                'venue': venue,
                'is_finished': False,  # These are upcoming games
                'home_score': None,  # No scores for upcoming games
                'away_score': None
            }
            
        except Exception as e:
            logger.error(f"Error extracting game details: {str(e)}")
            return None
    
    def _deduplicate_games(self, games: List[Dict]) -> List[Dict]:
        """Remove duplicate games based on teams, round, and season"""
        seen = set()
        unique_games = []
        
        for game in games:
            key = (
                game.get('home_team'),
                game.get('away_team'), 
                game.get('round'),
                game.get('season')
            )
            
            if key not in seen and all(key):
                seen.add(key)
                unique_games.append(game)
        
        return unique_games
    
    def save_upcoming_games_to_db(self, db: Session, games_data: Dict) -> Dict:
        """Save upcoming games to database"""
        try:
            if not games_data['success']:
                return games_data
            
            saved_count = 0
            updated_count = 0
            errors = []
            
            for game_data in games_data['games']:
                try:
                    # Check if game already exists
                    existing_game = db.query(Game).filter(
                        Game.home_team == game_data['home_team'],
                        Game.away_team == game_data['away_team'],
                        Game.round == game_data['round'],
                        Game.season == game_data['season']
                    ).first()
                    
                    if existing_game:
                        # Update existing game with new information
                        if game_data.get('game_date'):
                            existing_game.game_date = game_data['game_date']
                        if game_data.get('venue'):
                            existing_game.venue = game_data['venue']
                        existing_game.is_finished = False
                        updated_count += 1
                    else:
                        # Create new game
                        new_game = Game(
                            season=game_data['season'],
                            round=game_data['round'],
                            home_team=game_data['home_team'],
                            away_team=game_data['away_team'],
                            game_date=game_data.get('game_date'),
                            venue=game_data.get('venue'),
                            is_finished=False,
                            home_score=None,
                            away_score=None
                        )
                        db.add(new_game)
                        saved_count += 1
                
                except Exception as e:
                    errors.append(f"Error saving game {game_data.get('home_team')} vs {game_data.get('away_team')}: {str(e)}")
            
            db.commit()
            
            return {
                'success': True,
                'saved_count': saved_count,
                'updated_count': updated_count,
                'total_processed': len(games_data['games']),
                'errors': errors
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving upcoming games to database: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_current_round(self) -> Optional[int]:
        """Get the current AFL round number"""
        try:
            current_year = datetime.now().year
            current_date = datetime.now()
            
            # Get season data
            season_data = self._get_season_fixture(current_year)
            
            if not season_data['success']:
                return None
            
            # Find the current round based on dates
            for game in season_data['games']:
                game_date = game.get('game_date')
                if game_date and game_date >= current_date:
                    return game.get('round')
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting current round: {str(e)}")
            return None 