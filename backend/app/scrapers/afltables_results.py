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

class AFLTablesResultsScraper:
    """Specialized scraper for completed AFL game results from afltables.com"""
    
    def __init__(self):
        self.base_url = "https://afltables.com/afl"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_recent_results(self, weeks_back: int = 1) -> Dict:
        """
        Get completed AFL game results from the previous specified weeks
        
        Args:
            weeks_back: How many weeks back to look for completed games
            
        Returns:
            Dictionary with completed games data
        """
        try:
            current_year = datetime.now().year
            current_date = datetime.now()
            start_date = current_date - timedelta(weeks=weeks_back)
            
            logger.info(f"Scraping completed AFL games from {start_date.strftime('%Y-%m-%d')} to {current_date.strftime('%Y-%m-%d')}")
            
            # Get current season's results
            season_data = self._get_season_results(current_year)
            
            if not season_data['success']:
                return season_data
            
            # Filter for recently completed games only
            recent_results = []
            for game in season_data['games']:
                game_date = game.get('game_date')
                if (game_date and start_date <= game_date <= current_date and 
                    game.get('is_finished', False)):
                    recent_results.append(game)
            
            return {
                'success': True,
                'games': recent_results,
                'total_games': len(recent_results),
                'date_range': {
                    'start': start_date.strftime('%Y-%m-%d'),
                    'end': current_date.strftime('%Y-%m-%d')
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting recent results: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_season_results(self, season: int) -> Dict:
        """Get completed games with results from afltables.com"""
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
                
                # Look for game data in tables with team links and scores
                team_links = table.find_all('a', href=lambda x: x and 'teams/' in x)
                if len(team_links) >= 2:
                    # Parse completed games from this table
                    table_games = self._parse_results_table(table, season, current_round)
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
            logger.error(f"Error getting season results: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _parse_results_table(self, table, season: int, current_round: int = None) -> List[Dict]:
        """Parse a results table to extract completed game data with scores"""
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
                    
                    # Extract game details including scores
                    game_data = self._extract_result_details(row, away_row, season, current_round)
                    if game_data and self._has_valid_scores(game_data):
                        game_data['home_team'] = home_team
                        game_data['away_team'] = away_team
                        game_data['is_finished'] = True
                        games.append(game_data)
                    
                    i += 2  # Skip both rows
                    continue
            
            i += 1
        
        return games
    
    def _extract_result_details(self, home_row, away_row, season: int, round_num: int = None) -> Optional[Dict]:
        """Extract game details including scores from home and away team rows"""
        try:
            # Extract date and time information
            game_date = None
            venue = None
            home_score = None
            away_score = None
            attendance = None
            
            # Extract scores from both rows
            home_cells = home_row.find_all(['td', 'th'])
            away_cells = away_row.find_all(['td', 'th'])
            
            # Look for score in home team row (usually in the second or third column)
            for i, cell in enumerate(home_cells):
                cell_text = cell.get_text(strip=True)
                
                # Look for AFL score pattern (goals.behinds.total) or just total
                score_match = re.search(r'(\d+)\.(\d+)\.(\d+)', cell_text)
                if score_match:
                    goals = int(score_match.group(1))
                    behinds = int(score_match.group(2))
                    total = int(score_match.group(3))
                    home_score = total
                    break
                elif cell_text.isdigit() and len(cell_text) <= 3:
                    # Simple total score
                    home_score = int(cell_text)
                    break
            
            # Look for score in away team row
            for i, cell in enumerate(away_cells):
                cell_text = cell.get_text(strip=True)
                
                # Look for AFL score pattern (goals.behinds.total) or just total
                score_match = re.search(r'(\d+)\.(\d+)\.(\d+)', cell_text)
                if score_match:
                    goals = int(score_match.group(1))
                    behinds = int(score_match.group(2))
                    total = int(score_match.group(3))
                    away_score = total
                    break
                elif cell_text.isdigit() and len(cell_text) <= 3:
                    # Simple total score
                    away_score = int(cell_text)
                    break
            
            # Look for other game information in either row
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
                    
                    # Look for attendance
                    attendance_match = re.search(r'Attendance:\s*(\d+)', cell_text)
                    if attendance_match:
                        attendance = int(attendance_match.group(1))
            
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
                'home_score': home_score,
                'away_score': away_score,
                'attendance': attendance,
                'winner': self._determine_winner(home_score, away_score)
            }
            
        except Exception as e:
            logger.error(f"Error extracting result details: {str(e)}")
            return None
    
    def _has_valid_scores(self, game_data: Dict) -> bool:
        """Check if game data has valid scores (indicating it's a completed game)"""
        home_score = game_data.get('home_score')
        away_score = game_data.get('away_score')
        
        return (home_score is not None and away_score is not None and 
                isinstance(home_score, int) and isinstance(away_score, int) and
                home_score >= 0 and away_score >= 0)
    
    def _determine_winner(self, home_score: Optional[int], away_score: Optional[int]) -> Optional[str]:
        """Determine the winner of a game based on scores"""
        if home_score is None or away_score is None:
            return None
        
        if home_score > away_score:
            return 'home'
        elif away_score > home_score:
            return 'away'
        else:
            return 'draw'
    
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
    
    def save_results_to_db(self, db: Session, results_data: Dict) -> Dict:
        """Save completed game results to database"""
        try:
            if not results_data['success']:
                return results_data
            
            updated_count = 0
            errors = []
            
            for game_data in results_data['games']:
                try:
                    # Find existing game
                    existing_game = db.query(Game).filter(
                        Game.home_team == game_data['home_team'],
                        Game.away_team == game_data['away_team'],
                        Game.round == game_data['round'],
                        Game.season == game_data['season']
                    ).first()
                    
                    if existing_game:
                        # Update with results
                        existing_game.home_score = game_data['home_score']
                        existing_game.away_score = game_data['away_score']
                        existing_game.is_finished = True
                        
                        if game_data.get('game_date'):
                            existing_game.game_date = game_data['game_date']
                        if game_data.get('venue'):
                            existing_game.venue = game_data['venue']
                        if game_data.get('attendance'):
                            existing_game.attendance = game_data['attendance']
                        
                        # Determine winner
                        if game_data['home_score'] > game_data['away_score']:
                            existing_game.winner = existing_game.home_team
                        elif game_data['away_score'] > game_data['home_score']:
                            existing_game.winner = existing_game.away_team
                        else:
                            existing_game.winner = None  # Draw
                        
                        updated_count += 1
                    else:
                        # Create new completed game if it doesn't exist
                        new_game = Game(
                            season=game_data['season'],
                            round=game_data['round'],
                            home_team=game_data['home_team'],
                            away_team=game_data['away_team'],
                            home_score=game_data['home_score'],
                            away_score=game_data['away_score'],
                            game_date=game_data.get('game_date'),
                            venue=game_data.get('venue'),
                            attendance=game_data.get('attendance'),
                            is_finished=True
                        )
                        
                        # Determine winner
                        if game_data['home_score'] > game_data['away_score']:
                            new_game.winner = game_data['home_team']
                        elif game_data['away_score'] > game_data['home_score']:
                            new_game.winner = game_data['away_team']
                        else:
                            new_game.winner = None  # Draw
                        
                        db.add(new_game)
                        updated_count += 1
                
                except Exception as e:
                    errors.append(f"Error saving result {game_data.get('home_team')} vs {game_data.get('away_team')}: {str(e)}")
            
            db.commit()
            
            return {
                'success': True,
                'updated_count': updated_count,
                'total_processed': len(results_data['games']),
                'errors': errors
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving results to database: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_prediction_accuracy(self, db: Session) -> Dict:
        """Update prediction accuracy for recently completed games"""
        try:
            from app.models.prediction import Prediction
            
            # Get recent completed games (last 2 weeks)
            two_weeks_ago = datetime.now() - timedelta(weeks=2)
            recent_games = db.query(Game).filter(
                Game.is_finished == True,
                Game.game_date >= two_weeks_ago,
                Game.home_score.isnot(None),
                Game.away_score.isnot(None)
            ).all()
            
            updated_predictions = 0
            
            for game in recent_games:
                # Find predictions for this game
                predictions = db.query(Prediction).filter(
                    Prediction.game_id == game.id,
                    Prediction.is_correct.is_(None)  # Not yet evaluated
                ).all()
                
                for prediction in predictions:
                    # Determine if prediction was correct
                    actual_winner = None
                    if game.home_score > game.away_score:
                        actual_winner = game.home_team
                    elif game.away_score > game.home_score:
                        actual_winner = game.away_team
                    
                    # Check if predicted winner matches actual winner
                    predicted_winner = None
                    if prediction.predicted_winner_id:
                        # Get team name from team ID
                        team = db.query(Team).filter(Team.id == prediction.predicted_winner_id).first()
                        if team:
                            predicted_winner = team.name
                    
                    prediction.is_correct = (predicted_winner == actual_winner)
                    updated_predictions += 1
            
            db.commit()
            
            return {
                'success': True,
                'updated_predictions': updated_predictions,
                'games_processed': len(recent_games)
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating prediction accuracy: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            } 