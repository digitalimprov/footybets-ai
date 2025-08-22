from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.services.tip_service import TipService
from pydantic import BaseModel

router = APIRouter()

class TipResponse(BaseModel):
    game_id: int
    home_team: str
    away_team: str
    venue: Optional[str]
    game_date: Optional[str]
    round: Optional[int]
    season: int
    match_title: str
    has_prediction: bool
    summary: Optional[str] = None
    confidence_level: Optional[str] = None
    prediction: Optional[dict] = None
    betting_recommendation: Optional[dict] = None

class WeeklyTipsResponse(BaseModel):
    success: bool
    tips: List[TipResponse]
    total_games: int
    week_range: dict
    message: Optional[str] = None

class AccuracyStatsResponse(BaseModel):
    success: bool
    stats: dict
    message: Optional[str] = None

@router.get("/weekly", response_model=WeeklyTipsResponse)
async def get_weekly_tips(
    weeks_ahead: int = Query(1, description="Number of weeks ahead to get tips for"),
    db: Session = Depends(get_db)
):
    """Get AI-generated tips for upcoming games in the next week(s)"""
    try:
        tip_service = TipService()
        result = tip_service.get_weekly_tips(db, weeks_ahead=weeks_ahead)
        
        if result['success']:
            return WeeklyTipsResponse(**result)
        else:
            raise HTTPException(status_code=500, detail=result['error'])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting weekly tips: {str(e)}")

@router.get("/round/{round_number}")
async def get_round_tips(
    round_number: int,
    season: int = Query(None, description="Season year (defaults to current year)"),
    db: Session = Depends(get_db)
):
    """Get AI-generated tips for a specific round"""
    try:
        tip_service = TipService()
        result = tip_service.get_round_tips(db, round_number=round_number, season=season)
        
        if result['success']:
            return result
        else:
            raise HTTPException(status_code=500, detail=result['error'])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting round tips: {str(e)}")

@router.post("/generate")
async def generate_tips_for_upcoming_games(db: Session = Depends(get_db)):
    """Generate new AI tips for upcoming games that don't have predictions yet"""
    try:
        tip_service = TipService()
        result = tip_service.generate_tips_for_upcoming_games(db)
        
        if result['success']:
            return result
        else:
            raise HTTPException(status_code=500, detail=result['error'])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating tips: {str(e)}")

@router.get("/accuracy", response_model=AccuracyStatsResponse)
async def get_prediction_accuracy(
    days_back: int = Query(30, description="Number of days back to calculate accuracy"),
    db: Session = Depends(get_db)
):
    """Get accuracy statistics for recent predictions"""
    try:
        tip_service = TipService()
        result = tip_service.get_prediction_accuracy_stats(db, days_back=days_back)
        
        if result['success']:
            return AccuracyStatsResponse(**result)
        else:
            raise HTTPException(status_code=500, detail=result['error'])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting accuracy stats: {str(e)}")

@router.get("/current-round")
async def get_current_round_tips(db: Session = Depends(get_db)):
    """Get tips for the current AFL round"""
    try:
        from app.scrapers.afltables_upcoming import AFLTablesUpcomingScraper
        
        # Get current round number
        scraper = AFLTablesUpcomingScraper()
        current_round = scraper.get_current_round()
        
        if not current_round:
            raise HTTPException(status_code=404, detail="Could not determine current round")
        
        # Get tips for current round
        tip_service = TipService()
        result = tip_service.get_round_tips(db, round_number=current_round)
        
        if result['success']:
            return result
        else:
            raise HTTPException(status_code=500, detail=result['error'])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting current round tips: {str(e)}")

@router.get("/featured")
async def get_featured_tips(
    limit: int = Query(5, description="Number of featured tips to return"),
    db: Session = Depends(get_db)
):
    """Get featured tips for the homepage - highest confidence upcoming games"""
    try:
        tip_service = TipService()
        
        # Get weekly tips
        result = tip_service.get_weekly_tips(db, weeks_ahead=1)
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result['error'])
        
        tips = result.get('tips', [])
        
        # Filter tips with predictions and sort by confidence
        featured_tips = []
        for tip in tips:
            if tip.get('has_prediction') and tip.get('prediction', {}).get('confidence'):
                featured_tips.append(tip)
        
        # Sort by confidence (highest first) and limit
        featured_tips.sort(key=lambda x: x.get('prediction', {}).get('confidence', 0), reverse=True)
        featured_tips = featured_tips[:limit]
        
        return {
            'success': True,
            'featured_tips': featured_tips,
            'total_featured': len(featured_tips),
            'message': f'Top {len(featured_tips)} most confident predictions for this week'
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting featured tips: {str(e)}")

@router.get("/upcoming")
async def get_upcoming_tips(
    days_ahead: int = Query(7, description="Number of days ahead to look for tips"),
    db: Session = Depends(get_db)
):
    """Get tips for games in the next specified days"""
    try:
        # Calculate date range
        start_date = datetime.now()
        end_date = start_date + timedelta(days=days_ahead)
        
        from app.models.game import Game
        from app.models.prediction import Prediction
        
        # Get upcoming games in date range
        upcoming_games = db.query(Game).filter(
            Game.is_finished == False,
            Game.game_date > start_date,
            Game.game_date <= end_date
        ).order_by(Game.game_date).all()
        
        if not upcoming_games:
            return {
                'success': True,
                'tips': [],
                'message': f'No upcoming games found in the next {days_ahead} days',
                'date_range': {
                    'start': start_date.strftime('%Y-%m-%d'),
                    'end': end_date.strftime('%Y-%m-%d')
                }
            }
        
        # Format tips
        tip_service = TipService()
        formatted_tips = []
        for game in upcoming_games:
            tip = tip_service._format_game_tip(db, game)
            if tip:
                formatted_tips.append(tip)
        
        return {
            'success': True,
            'tips': formatted_tips,
            'total_games': len(formatted_tips),
            'date_range': {
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d')
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting upcoming tips: {str(e)}")

@router.get("/game/{game_id}")
async def get_game_tip(
    game_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed tip for a specific game"""
    try:
        from app.models.game import Game
        
        # Get the game
        game = db.query(Game).filter(Game.id == game_id).first()
        
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        # Format the tip
        tip_service = TipService()
        tip = tip_service._format_game_tip(db, game)
        
        if not tip:
            raise HTTPException(status_code=500, detail="Could not format tip for this game")
        
        return {
            'success': True,
            'tip': tip
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting game tip: {str(e)}") 