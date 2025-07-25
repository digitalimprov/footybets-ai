import google.generativeai as genai
import json
import pandas as pd
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.config import settings
from app.models.game import Game
from app.models.team import Team
from app.models.prediction import Prediction
import logging

logger = logging.getLogger(__name__)

class AFLPredictor:
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.model_version = "1.0.0"
        
    def generate_predictions(self, db: Session, upcoming_games: List[Game]) -> List[Prediction]:
        """Generate predictions for upcoming games"""
        predictions = []
        
        for game in upcoming_games:
            try:
                prediction = self._predict_single_game(db, game)
                if prediction:
                    predictions.append(prediction)
                    
            except Exception as e:
                logger.error(f"Error predicting game {game.id}: {e}")
                
        return predictions
    
    def _predict_single_game(self, db: Session, game: Game) -> Optional[Prediction]:
        """Generate prediction for a single game"""
        try:
            # Get historical data for both teams
            home_team_data = self._get_team_historical_data(db, game.home_team_id)
            away_team_data = self._get_team_historical_data(db, game.away_team_id)
            
            # Get head-to-head data
            h2h_data = self._get_head_to_head_data(db, game.home_team_id, game.away_team_id)
            
            # Get recent form data
            home_recent_form = self._get_recent_form(db, game.home_team_id)
            away_recent_form = self._get_recent_form(db, game.away_team_id)
            
            # Prepare context for AI
            context = self._prepare_prediction_context(
                game, home_team_data, away_team_data, h2h_data, home_recent_form, away_recent_form
            )
            
            # Generate prediction using Gemini
            prediction_result = self._call_gemini_for_prediction(context)
            
            # Parse and create prediction object
            prediction = self._create_prediction_object(game, prediction_result)
            
            return prediction
            
        except Exception as e:
            logger.error(f"Error in single game prediction: {e}")
            return None
    
    def _get_team_historical_data(self, db: Session, team_id: int) -> Dict:
        """Get historical performance data for a team"""
        # Get last 2 seasons of data
        two_years_ago = datetime.now().year - 2
        
        games = db.query(Game).filter(
            (Game.home_team_id == team_id) | (Game.away_team_id == team_id),
            Game.season >= two_years_ago,
            Game.is_finished == True
        ).all()
        
        stats = {
            'total_games': len(games),
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'home_games': 0,
            'away_games': 0,
            'home_wins': 0,
            'away_wins': 0,
            'avg_score_for': 0,
            'avg_score_against': 0,
            'recent_games': []
        }
        
        total_score_for = 0
        total_score_against = 0
        
        for game in games:
            is_home = game.home_team_id == team_id
            team_score = game.home_score if is_home else game.away_score
            opponent_score = game.away_score if is_home else game.home_score
            
            total_score_for += team_score
            total_score_against += opponent_score
            
            if is_home:
                stats['home_games'] += 1
                if team_score > opponent_score:
                    stats['home_wins'] += 1
                    stats['wins'] += 1
                elif team_score < opponent_score:
                    stats['losses'] += 1
                else:
                    stats['draws'] += 1
            else:
                stats['away_games'] += 1
                if team_score > opponent_score:
                    stats['away_wins'] += 1
                    stats['wins'] += 1
                elif team_score < opponent_score:
                    stats['losses'] += 1
                else:
                    stats['draws'] += 1
            
            # Add recent games (last 10)
            if len(stats['recent_games']) < 10:
                stats['recent_games'].append({
                    'date': game.game_date,
                    'opponent': game.away_team.name if is_home else game.home_team.name,
                    'score_for': team_score,
                    'score_against': opponent_score,
                    'result': 'W' if team_score > opponent_score else 'L' if team_score < opponent_score else 'D',
                    'venue': 'home' if is_home else 'away'
                })
        
        if stats['total_games'] > 0:
            stats['avg_score_for'] = total_score_for / stats['total_games']
            stats['avg_score_against'] = total_score_against / stats['total_games']
        
        return stats
    
    def _get_head_to_head_data(self, db: Session, team1_id: int, team2_id: int) -> Dict:
        """Get head-to-head statistics between two teams"""
        games = db.query(Game).filter(
            Game.is_finished == True,
            ((Game.home_team_id == team1_id) & (Game.away_team_id == team2_id)) |
            ((Game.home_team_id == team2_id) & (Game.away_team_id == team1_id))
        ).order_by(Game.game_date.desc()).limit(10).all()
        
        h2h_stats = {
            'total_games': len(games),
            'team1_wins': 0,
            'team2_wins': 0,
            'draws': 0,
            'recent_games': []
        }
        
        for game in games:
            team1_score = game.home_score if game.home_team_id == team1_id else game.away_score
            team2_score = game.away_score if game.home_team_id == team1_id else game.home_score
            
            if team1_score > team2_score:
                h2h_stats['team1_wins'] += 1
            elif team2_score > team1_score:
                h2h_stats['team2_wins'] += 1
            else:
                h2h_stats['draws'] += 1
            
            h2h_stats['recent_games'].append({
                'date': game.game_date,
                'team1_score': team1_score,
                'team2_score': team2_score,
                'venue': game.venue
            })
        
        return h2h_stats
    
    def _get_recent_form(self, db: Session, team_id: int) -> List[Dict]:
        """Get recent form for a team (last 5 games)"""
        recent_games = db.query(Game).filter(
            (Game.home_team_id == team_id) | (Game.away_team_id == team_id),
            Game.is_finished == True
        ).order_by(Game.game_date.desc()).limit(5).all()
        
        form = []
        for game in recent_games:
            is_home = game.home_team_id == team_id
            team_score = game.home_score if is_home else game.away_score
            opponent_score = game.away_score if is_home else game.home_score
            
            form.append({
                'result': 'W' if team_score > opponent_score else 'L' if team_score < opponent_score else 'D',
                'score_for': team_score,
                'score_against': opponent_score,
                'margin': team_score - opponent_score
            })
        
        return form
    
    def _prepare_prediction_context(self, game: Game, home_data: Dict, away_data: Dict, 
                                  h2h_data: Dict, home_form: List, away_form: List) -> str:
        """Prepare context string for AI prediction"""
        home_team = game.home_team
        away_team = game.away_team
        
        context = f"""
        AFL Game Prediction Analysis
        
        Upcoming Game:
        {home_team.name} (Home) vs {away_team.name} (Away)
        Venue: {game.venue}
        Date: {game.game_date}
        
        {home_team.name} Historical Performance (Last 2 seasons):
        - Total Games: {home_data['total_games']}
        - Wins: {home_data['wins']}, Losses: {home_data['losses']}, Draws: {home_data['draws']}
        - Home Games: {home_data['home_games']}, Home Wins: {home_data['home_wins']}
        - Average Score For: {home_data['avg_score_for']:.1f}
        - Average Score Against: {home_data['avg_score_against']:.1f}
        
        {away_team.name} Historical Performance (Last 2 seasons):
        - Total Games: {away_data['total_games']}
        - Wins: {away_data['wins']}, Losses: {away_data['losses']}, Draws: {away_data['draws']}
        - Away Games: {away_data['away_games']}, Away Wins: {away_data['away_wins']}
        - Average Score For: {away_data['avg_score_for']:.1f}
        - Average Score Against: {away_data['avg_score_against']:.1f}
        
        Head-to-Head Record (Last 10 games):
        - Total Games: {h2h_data['total_games']}
        - {home_team.name} Wins: {h2h_data['team1_wins']}
        - {away_team.name} Wins: {h2h_data['team2_wins']}
        - Draws: {h2h_data['draws']}
        
        {home_team.name} Recent Form (Last 5 games):
        {', '.join([game['result'] for game in home_form])}
        
        {away_team.name} Recent Form (Last 5 games):
        {', '.join([game['result'] for game in away_form])}
        
        Based on this historical data, predict:
        1. The likely winner
        2. Predicted final scores
        3. Confidence level (0-100%)
        4. Key factors influencing the prediction
        5. Betting recommendation (if any)
        
        Provide your analysis in JSON format with the following structure:
        {{
            "predicted_winner": "home" or "away",
            "predicted_home_score": integer,
            "predicted_away_score": integer,
            "confidence_score": float (0.0-1.0),
            "reasoning": "detailed explanation",
            "key_factors": ["factor1", "factor2", "factor3"],
            "betting_recommendation": "home", "away", "draw", or "none",
            "bet_confidence": float (0.0-1.0)
        }}
        """
        
        return context
    
    def _call_gemini_for_prediction(self, context: str) -> Dict:
        """Call Google Gemini API for prediction"""
        try:
            response = self.model.generate_content(context)
            
            # Extract JSON from response
            response_text = response.text
            
            # Try to find JSON in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Fallback: try to parse the entire response
                return json.loads(response_text)
                
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            # Return default prediction
            return {
                "predicted_winner": "home",
                "predicted_home_score": 100,
                "predicted_away_score": 90,
                "confidence_score": 0.5,
                "reasoning": "Default prediction due to API error",
                "key_factors": ["Historical data", "Team form", "Venue advantage"],
                "betting_recommendation": "none",
                "bet_confidence": 0.3
            }
    
    def _create_prediction_object(self, game: Game, prediction_data: Dict) -> Prediction:
        """Create Prediction object from AI response"""
        predicted_winner_id = game.home_team_id if prediction_data.get('predicted_winner') == 'home' else game.away_team_id
        
        return Prediction(
            game_id=game.id,
            predicted_winner_id=predicted_winner_id,
            confidence_score=prediction_data.get('confidence_score', 0.5),
            predicted_home_score=prediction_data.get('predicted_home_score', 0),
            predicted_away_score=prediction_data.get('predicted_away_score', 0),
            reasoning=prediction_data.get('reasoning', ''),
            factors_considered=json.dumps(prediction_data.get('key_factors', [])),
            recommended_bet=prediction_data.get('betting_recommendation', 'none'),
            bet_confidence=prediction_data.get('bet_confidence', 0.0),
            odds_analysis=json.dumps({}),  # Placeholder for odds analysis
            model_version=self.model_version
        )
    
    def update_prediction_accuracy(self, db: Session):
        """Update prediction accuracy for completed games"""
        # Get predictions for completed games that haven't been evaluated
        predictions = db.query(Prediction).join(Game).filter(
            Game.is_finished == True,
            Prediction.is_correct.is_(None)
        ).all()
        
        for prediction in predictions:
            game = prediction.game
            
            # Determine actual winner
            if game.home_score > game.away_score:
                actual_winner_id = game.home_team_id
            elif game.away_score > game.home_score:
                actual_winner_id = game.away_team_id
            else:
                actual_winner_id = None  # Draw
            
            # Check if prediction was correct
            if actual_winner_id is None:
                # Draw - prediction is correct if it predicted a draw
                prediction.is_correct = (prediction.recommended_bet == 'draw')
            else:
                prediction.is_correct = (prediction.predicted_winner_id == actual_winner_id)
        
        db.commit()
        logger.info(f"Updated accuracy for {len(predictions)} predictions") 