from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.models.prediction import Prediction
from app.models.game import Game
from app.models.team import Team
from app.ai.predictor import AFLPredictor
import logging

logger = logging.getLogger(__name__)

class TipService:
    """Service for managing and formatting AI-generated tips for users"""
    
    def __init__(self):
        self.predictor = AFLPredictor()
    
    def get_weekly_tips(self, db: Session, weeks_ahead: int = 1) -> Dict:
        """Get formatted tips for upcoming games in the next week(s)"""
        try:
            # Calculate date range
            start_date = datetime.now()
            end_date = start_date + timedelta(weeks=weeks_ahead)
            
            # Get upcoming games with predictions
            upcoming_games_query = db.query(Game).filter(
                Game.is_finished == False,
                Game.game_date > start_date,
                Game.game_date <= end_date
            ).order_by(Game.game_date)
            
            upcoming_games = upcoming_games_query.all()
            
            if not upcoming_games:
                return {
                    'success': True,
                    'tips': [],
                    'message': 'No upcoming games found for the specified period',
                    'week_range': {
                        'start': start_date.strftime('%Y-%m-%d'),
                        'end': end_date.strftime('%Y-%m-%d')
                    }
                }
            
            # Format tips for each game
            formatted_tips = []
            for game in upcoming_games:
                tip = self._format_game_tip(db, game)
                if tip:
                    formatted_tips.append(tip)
            
            return {
                'success': True,
                'tips': formatted_tips,
                'total_games': len(formatted_tips),
                'week_range': {
                    'start': start_date.strftime('%Y-%m-%d'),
                    'end': end_date.strftime('%Y-%m-%d')
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting weekly tips: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_round_tips(self, db: Session, round_number: int, season: int = None) -> Dict:
        """Get tips for a specific round"""
        try:
            if not season:
                season = datetime.now().year
            
            # Get games for the specified round
            round_games = db.query(Game).filter(
                Game.round == round_number,
                Game.season == season
            ).order_by(Game.game_date).all()
            
            if not round_games:
                return {
                    'success': True,
                    'tips': [],
                    'message': f'No games found for Round {round_number} of {season}',
                    'round': round_number,
                    'season': season
                }
            
            # Format tips for each game
            formatted_tips = []
            for game in round_games:
                tip = self._format_game_tip(db, game)
                if tip:
                    formatted_tips.append(tip)
            
            return {
                'success': True,
                'tips': formatted_tips,
                'total_games': len(formatted_tips),
                'round': round_number,
                'season': season
            }
            
        except Exception as e:
            logger.error(f"Error getting round tips: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _format_game_tip(self, db: Session, game: Game) -> Optional[Dict]:
        """Format a single game into a user-friendly tip"""
        try:
            # Get the latest prediction for this game
            prediction = db.query(Prediction).filter(
                Prediction.game_id == game.id
            ).order_by(Prediction.prediction_date.desc()).first()
            
            # Basic game info
            tip = {
                'game_id': game.id,
                'home_team': game.home_team,
                'away_team': game.away_team,
                'venue': game.venue,
                'game_date': game.game_date.isoformat() if game.game_date else None,
                'round': game.round,
                'season': game.season,
                'match_title': f"{game.home_team} vs {game.away_team}",
                'has_prediction': prediction is not None
            }
            
            if prediction:
                # Get predicted winner team name
                predicted_winner_name = None
                if prediction.predicted_winner_id:
                    winner_team = db.query(Team).filter(Team.id == prediction.predicted_winner_id).first()
                    if winner_team:
                        predicted_winner_name = winner_team.name
                
                # Format the prediction
                tip.update({
                    'prediction': {
                        'winner': predicted_winner_name,
                        'confidence': round(prediction.confidence_score * 100, 1) if prediction.confidence_score else None,
                        'predicted_score': {
                            'home': prediction.predicted_home_score,
                            'away': prediction.predicted_away_score
                        },
                        'margin': abs(prediction.predicted_home_score - prediction.predicted_away_score) if prediction.predicted_home_score and prediction.predicted_away_score else None,
                        'reasoning': prediction.reasoning,
                        'recommended_bet': prediction.recommended_bet,
                        'bet_confidence': round(prediction.bet_confidence * 100, 1) if prediction.bet_confidence else None,
                        'model_version': prediction.model_version,
                        'generated_date': prediction.prediction_date.isoformat() if prediction.prediction_date else None
                    }
                })
                
                # Add user-friendly summary
                tip['summary'] = self._create_tip_summary(tip)
                
                # Add confidence level description
                tip['confidence_level'] = self._get_confidence_description(prediction.confidence_score)
                
                # Add betting recommendation
                tip['betting_recommendation'] = self._create_betting_recommendation(prediction)
            
            return tip
            
        except Exception as e:
            logger.error(f"Error formatting game tip: {str(e)}")
            return None
    
    def _create_tip_summary(self, tip: Dict) -> str:
        """Create a user-friendly summary of the tip"""
        try:
            prediction = tip.get('prediction', {})
            winner = prediction.get('winner')
            confidence = prediction.get('confidence')
            margin = prediction.get('margin')
            
            if not winner:
                return f"No clear prediction available for {tip['match_title']}"
            
            summary = f"**{winner}** to win"
            
            if confidence:
                summary += f" ({confidence}% confidence)"
            
            if margin and margin > 0:
                if margin <= 6:
                    summary += f" in a close contest (margin: {margin} points)"
                elif margin <= 20:
                    summary += f" by {margin} points"
                else:
                    summary += f" comfortably by {margin} points"
            
            return summary
            
        except Exception as e:
            logger.error(f"Error creating tip summary: {str(e)}")
            return "Prediction summary unavailable"
    
    def _get_confidence_description(self, confidence_score: float) -> str:
        """Convert confidence score to user-friendly description"""
        if not confidence_score:
            return "Unknown"
        
        confidence_pct = confidence_score * 100
        
        if confidence_pct >= 80:
            return "Very High"
        elif confidence_pct >= 65:
            return "High"
        elif confidence_pct >= 50:
            return "Moderate"
        elif confidence_pct >= 35:
            return "Low"
        else:
            return "Very Low"
    
    def _create_betting_recommendation(self, prediction: Prediction) -> Dict:
        """Create betting recommendation based on prediction"""
        try:
            recommendation = {
                'type': prediction.recommended_bet,
                'confidence': round(prediction.bet_confidence * 100, 1) if prediction.bet_confidence else None,
                'recommendation': "No recommendation"
            }
            
            if prediction.recommended_bet == "none":
                recommendation['recommendation'] = "No strong betting opportunity identified"
            elif prediction.recommended_bet in ["home", "away"]:
                team = "home team" if prediction.recommended_bet == "home" else "away team"
                confidence = prediction.bet_confidence or 0
                
                if confidence >= 0.7:
                    recommendation['recommendation'] = f"Strong bet on {team}"
                elif confidence >= 0.6:
                    recommendation['recommendation'] = f"Good bet on {team}"
                elif confidence >= 0.5:
                    recommendation['recommendation'] = f"Consider betting on {team}"
                else:
                    recommendation['recommendation'] = f"Weak betting opportunity on {team}"
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Error creating betting recommendation: {str(e)}")
            return {
                'type': 'none',
                'confidence': None,
                'recommendation': "Betting recommendation unavailable"
            }
    
    def generate_tips_for_upcoming_games(self, db: Session) -> Dict:
        """Generate new tips for games that don't have predictions yet"""
        try:
            # Get upcoming games without recent predictions
            one_week_ahead = datetime.now() + timedelta(weeks=1)
            upcoming_games = db.query(Game).filter(
                Game.is_finished == False,
                Game.game_date > datetime.now(),
                Game.game_date <= one_week_ahead
            ).all()
            
            games_needing_predictions = []
            for game in upcoming_games:
                # Check if we have a recent prediction
                recent_prediction = db.query(Prediction).filter(
                    Prediction.game_id == game.id,
                    Prediction.prediction_date >= datetime.now() - timedelta(days=1)
                ).first()
                
                if not recent_prediction:
                    games_needing_predictions.append(game)
            
            if not games_needing_predictions:
                return {
                    'success': True,
                    'message': 'All upcoming games already have recent predictions',
                    'predictions_generated': 0
                }
            
            # Generate predictions
            predictions = self.predictor.generate_predictions(db, games_needing_predictions)
            
            # Save predictions
            predictions_saved = 0
            for prediction in predictions:
                db.add(prediction)
                predictions_saved += 1
            
            db.commit()
            
            return {
                'success': True,
                'message': f'Generated {predictions_saved} new predictions',
                'predictions_generated': predictions_saved,
                'games_processed': len(games_needing_predictions)
            }
            
        except Exception as e:
            logger.error(f"Error generating tips: {str(e)}")
            db.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_prediction_accuracy_stats(self, db: Session, days_back: int = 30) -> Dict:
        """Get accuracy statistics for recent predictions"""
        try:
            start_date = datetime.now() - timedelta(days=days_back)
            
            # Get completed predictions from the specified period
            completed_predictions = db.query(Prediction).join(Game).filter(
                Game.is_finished == True,
                Prediction.prediction_date >= start_date,
                Prediction.is_correct.isnot(None)
            ).all()
            
            if not completed_predictions:
                return {
                    'success': True,
                    'stats': {
                        'total_predictions': 0,
                        'accuracy_rate': 0,
                        'correct_predictions': 0,
                        'incorrect_predictions': 0
                    },
                    'message': f'No completed predictions found in the last {days_back} days'
                }
            
            # Calculate statistics
            total = len(completed_predictions)
            correct = len([p for p in completed_predictions if p.is_correct])
            incorrect = total - correct
            accuracy_rate = (correct / total) * 100 if total > 0 else 0
            
            return {
                'success': True,
                'stats': {
                    'total_predictions': total,
                    'accuracy_rate': round(accuracy_rate, 1),
                    'correct_predictions': correct,
                    'incorrect_predictions': incorrect,
                    'period_days': days_back
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting accuracy stats: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            } 