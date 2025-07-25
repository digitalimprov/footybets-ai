from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.prediction import Prediction
from app.models.game import Game
from app.models.team import Team
from app.ai.predictor import AFLPredictor
from pydantic import BaseModel

router = APIRouter()

class PredictionResponse(BaseModel):
    id: int
    game_id: int
    home_team_name: str
    away_team_name: str
    predicted_winner_name: str
    confidence_score: float
    predicted_home_score: int
    predicted_away_score: int
    reasoning: str
    factors_considered: List[str]
    recommended_bet: str
    bet_confidence: float
    model_version: str
    prediction_date: datetime
    is_correct: Optional[bool] = None
    
    class Config:
        from_attributes = True

class UserTipRequest(BaseModel):
    game_id: int
    user_name: str
    user_email: str
    predicted_winner_id: int
    predicted_home_score: int
    predicted_away_score: int
    reasoning: str

@router.get("/", response_model=List[PredictionResponse])
async def get_predictions(
    game_id: Optional[int] = Query(None, description="Filter by game ID"),
    season: Optional[int] = Query(None, description="Filter by season"),
    limit: int = Query(50, description="Number of predictions to return"),
    db: Session = Depends(get_db)
):
    """Get AI predictions with optional filtering"""
    query = db.query(Prediction).join(Game).join(
        Team, Game.home_team_id == Team.id
    ).join(Team, Game.away_team_id == Team.id)
    
    if game_id:
        query = query.filter(Prediction.game_id == game_id)
    
    if season:
        query = query.join(Game).filter(Game.season == season)
    
    predictions = query.order_by(Prediction.prediction_date.desc()).limit(limit).all()
    
    response_predictions = []
    for pred in predictions:
        response_predictions.append(PredictionResponse(
            id=pred.id,
            game_id=pred.game_id,
            home_team_name=pred.game.home_team.name,
            away_team_name=pred.game.away_team.name,
            predicted_winner_name=pred.predicted_winner.name,
            confidence_score=pred.confidence_score,
            predicted_home_score=pred.predicted_home_score,
            predicted_away_score=pred.predicted_away_score,
            reasoning=pred.reasoning,
            factors_considered=pred.factors_considered.split(',') if pred.factors_considered else [],
            recommended_bet=pred.recommended_bet,
            bet_confidence=pred.bet_confidence,
            model_version=pred.model_version,
            prediction_date=pred.prediction_date,
            is_correct=pred.is_correct
        ))
    
    return response_predictions

@router.get("/upcoming", response_model=List[PredictionResponse])
async def get_upcoming_predictions(
    days: int = Query(7, description="Number of days ahead to look"),
    db: Session = Depends(get_db)
):
    """Get predictions for upcoming games"""
    future_date = datetime.now() + timedelta(days=days)
    
    predictions = db.query(Prediction).join(Game).filter(
        Game.is_finished == False,
        Game.game_date > datetime.now(),
        Game.game_date <= future_date
    ).order_by(Game.game_date.asc()).all()
    
    response_predictions = []
    for pred in predictions:
        response_predictions.append(PredictionResponse(
            id=pred.id,
            game_id=pred.game_id,
            home_team_name=pred.game.home_team.name,
            away_team_name=pred.game.away_team.name,
            predicted_winner_name=pred.predicted_winner.name,
            confidence_score=pred.confidence_score,
            predicted_home_score=pred.predicted_home_score,
            predicted_away_score=pred.predicted_away_score,
            reasoning=pred.reasoning,
            factors_considered=pred.factors_considered.split(',') if pred.factors_considered else [],
            recommended_bet=pred.recommended_bet,
            bet_confidence=pred.bet_confidence,
            model_version=pred.model_version,
            prediction_date=pred.prediction_date,
            is_correct=pred.is_correct
        ))
    
    return response_predictions

@router.post("/generate")
async def generate_predictions(
    days: int = Query(7, description="Generate predictions for next N days"),
    db: Session = Depends(get_db)
):
    """Generate new AI predictions for upcoming games"""
    try:
        # Get upcoming games
        future_date = datetime.now() + timedelta(days=days)
        upcoming_games = db.query(Game).filter(
            Game.is_finished == False,
            Game.game_date > datetime.now(),
            Game.game_date <= future_date
        ).all()
        
        if not upcoming_games:
            return {"message": "No upcoming games found", "predictions_generated": 0}
        
        # Initialize predictor
        predictor = AFLPredictor()
        
        # Generate predictions
        predictions = predictor.generate_predictions(db, upcoming_games)
        
        # Save predictions to database
        for prediction in predictions:
            db.add(prediction)
        
        db.commit()
        
        return {
            "message": f"Generated {len(predictions)} predictions",
            "predictions_generated": len(predictions),
            "games_processed": len(upcoming_games)
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating predictions: {str(e)}")

@router.post("/update-accuracy")
async def update_prediction_accuracy(db: Session = Depends(get_db)):
    """Update prediction accuracy for completed games"""
    try:
        predictor = AFLPredictor()
        predictor.update_prediction_accuracy(db)
        
        return {"message": "Prediction accuracy updated successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating accuracy: {str(e)}")

@router.get("/{prediction_id}", response_model=PredictionResponse)
async def get_prediction(prediction_id: int, db: Session = Depends(get_db)):
    """Get a specific prediction by ID"""
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    
    return PredictionResponse(
        id=prediction.id,
        game_id=prediction.game_id,
        home_team_name=prediction.game.home_team.name,
        away_team_name=prediction.game.away_team.name,
        predicted_winner_name=prediction.predicted_winner.name,
        confidence_score=prediction.confidence_score,
        predicted_home_score=prediction.predicted_home_score,
        predicted_away_score=prediction.predicted_away_score,
        reasoning=prediction.reasoning,
        factors_considered=prediction.factors_considered.split(',') if prediction.factors_considered else [],
        recommended_bet=prediction.recommended_bet,
        bet_confidence=prediction.bet_confidence,
        model_version=prediction.model_version,
        prediction_date=prediction.prediction_date,
        is_correct=prediction.is_correct
    ) 