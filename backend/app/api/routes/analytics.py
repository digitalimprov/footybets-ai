from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.prediction import Prediction
from app.models.game import Game
from app.models.analytics import Analytics
from pydantic import BaseModel

router = APIRouter()

class AnalyticsResponse(BaseModel):
    period_type: str
    period_start: datetime
    period_end: datetime
    total_predictions: int
    correct_predictions: int
    accuracy_percentage: float
    high_confidence_accuracy: float
    medium_confidence_accuracy: float
    low_confidence_accuracy: float
    total_bets_recommended: int
    winning_bets: int
    betting_roi: float
    model_version: str
    average_confidence: float

class TeamPerformanceResponse(BaseModel):
    team_name: str
    total_games: int
    wins: int
    losses: int
    draws: int
    win_percentage: float
    avg_score_for: float
    avg_score_against: float

@router.get("/overview", response_model=AnalyticsResponse)
async def get_analytics_overview(
    period: str = Query("all", description="Time period: 'all', 'season', 'month', 'week'"),
    season: Optional[int] = Query(None, description="Specific season"),
    db: Session = Depends(get_db)
):
    """Get overall analytics overview"""
    try:
        # Calculate date range based on period
        now = datetime.now()
        if period == "week":
            start_date = now - timedelta(days=7)
        elif period == "month":
            start_date = now - timedelta(days=30)
        elif period == "season":
            start_date = datetime(now.year, 1, 1)
        else:  # all
            start_date = datetime(2000, 1, 1)
        
        # Get predictions in date range
        query = db.query(Prediction).join(Game).filter(
            Prediction.prediction_date >= start_date,
            Prediction.is_correct.isnot(None)
        )
        
        if season:
            query = query.filter(Game.season == season)
        
        predictions = query.all()
        
        if not predictions:
            return AnalyticsResponse(
                period_type=period,
                period_start=start_date,
                period_end=now,
                total_predictions=0,
                correct_predictions=0,
                accuracy_percentage=0.0,
                high_confidence_accuracy=0.0,
                medium_confidence_accuracy=0.0,
                low_confidence_accuracy=0.0,
                total_bets_recommended=0,
                winning_bets=0,
                betting_roi=0.0,
                model_version="1.0.0",
                average_confidence=0.0
            )
        
        # Calculate statistics
        total_predictions = len(predictions)
        correct_predictions = sum(1 for p in predictions if p.is_correct)
        accuracy_percentage = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0
        
        # Confidence level breakdown
        high_confidence = [p for p in predictions if p.confidence_score > 0.8]
        medium_confidence = [p for p in predictions if 0.6 <= p.confidence_score <= 0.8]
        low_confidence = [p for p in predictions if p.confidence_score < 0.6]
        
        high_confidence_accuracy = (sum(1 for p in high_confidence if p.is_correct) / len(high_confidence) * 100) if high_confidence else 0
        medium_confidence_accuracy = (sum(1 for p in medium_confidence if p.is_correct) / len(medium_confidence) * 100) if medium_confidence else 0
        low_confidence_accuracy = (sum(1 for p in low_confidence if p.is_correct) / len(low_confidence) * 100) if low_confidence else 0
        
        # Betting statistics
        bets_recommended = [p for p in predictions if p.recommended_bet in ['home', 'away']]
        total_bets_recommended = len(bets_recommended)
        winning_bets = sum(1 for p in bets_recommended if p.is_correct)
        betting_roi = ((winning_bets / total_bets_recommended) - 0.5) * 100 if total_bets_recommended > 0 else 0
        
        # Average confidence
        average_confidence = sum(p.confidence_score for p in predictions) / total_predictions if total_predictions > 0 else 0
        
        return AnalyticsResponse(
            period_type=period,
            period_start=start_date,
            period_end=now,
            total_predictions=total_predictions,
            correct_predictions=correct_predictions,
            accuracy_percentage=accuracy_percentage,
            high_confidence_accuracy=high_confidence_accuracy,
            medium_confidence_accuracy=medium_confidence_accuracy,
            low_confidence_accuracy=low_confidence_accuracy,
            total_bets_recommended=total_bets_recommended,
            winning_bets=winning_bets,
            betting_roi=betting_roi,
            model_version="1.0.0",
            average_confidence=average_confidence
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating analytics: {str(e)}")

@router.get("/team-performance", response_model=List[TeamPerformanceResponse])
async def get_team_performance(
    season: Optional[int] = Query(None, description="Filter by season"),
    limit: int = Query(18, description="Number of teams to return"),
    db: Session = Depends(get_db)
):
    """Get team performance statistics"""
    try:
        # Get all teams with their game statistics
        from app.models.team import Team
        
        query = db.query(Team).join(Game, or_(Game.home_team_id == Team.id, Game.away_team_id == Team.id))
        
        if season:
            query = query.filter(Game.season == season)
        
        teams = query.distinct().limit(limit).all()
        
        team_performance = []
        for team in teams:
            # Get team's games
            team_games = db.query(Game).filter(
                or_(Game.home_team_id == team.id, Game.away_team_id == team.id),
                Game.is_finished == True
            )
            
            if season:
                team_games = team_games.filter(Game.season == season)
            
            team_games = team_games.all()
            
            if not team_games:
                continue
            
            # Calculate statistics
            total_games = len(team_games)
            wins = 0
            losses = 0
            draws = 0
            total_score_for = 0
            total_score_against = 0
            
            for game in team_games:
                is_home = game.home_team_id == team.id
                team_score = game.home_score if is_home else game.away_score
                opponent_score = game.away_score if is_home else game.home_score
                
                total_score_for += team_score
                total_score_against += opponent_score
                
                if team_score > opponent_score:
                    wins += 1
                elif team_score < opponent_score:
                    losses += 1
                else:
                    draws += 1
            
            win_percentage = (wins / total_games) * 100 if total_games > 0 else 0
            avg_score_for = total_score_for / total_games if total_games > 0 else 0
            avg_score_against = total_score_against / total_games if total_games > 0 else 0
            
            team_performance.append(TeamPerformanceResponse(
                team_name=team.name,
                total_games=total_games,
                wins=wins,
                losses=losses,
                draws=draws,
                win_percentage=win_percentage,
                avg_score_for=avg_score_for,
                avg_score_against=avg_score_against
            ))
        
        # Sort by win percentage
        team_performance.sort(key=lambda x: x.win_percentage, reverse=True)
        
        return team_performance
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating team performance: {str(e)}")

@router.get("/prediction-trends")
async def get_prediction_trends(
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db)
):
    """Get prediction accuracy trends over time"""
    try:
        start_date = datetime.now() - timedelta(days=days)
        
        # Get predictions grouped by date
        daily_stats = db.query(
            func.date(Prediction.prediction_date).label('date'),
            func.count(Prediction.id).label('total_predictions'),
            func.sum(func.case([(Prediction.is_correct == True, 1)], else_=0)).label('correct_predictions')
        ).filter(
            Prediction.prediction_date >= start_date,
            Prediction.is_correct.isnot(None)
        ).group_by(func.date(Prediction.prediction_date)).order_by(func.date(Prediction.prediction_date)).all()
        
        trends = []
        for stat in daily_stats:
            accuracy = (stat.correct_predictions / stat.total_predictions * 100) if stat.total_predictions > 0 else 0
            trends.append({
                'date': stat.date.isoformat(),
                'total_predictions': stat.total_predictions,
                'correct_predictions': stat.correct_predictions,
                'accuracy_percentage': accuracy
            })
        
        return trends
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating prediction trends: {str(e)}")

@router.post("/generate-analytics")
async def generate_analytics(
    period_type: str = Query("weekly", description="Period type: daily, weekly, monthly"),
    db: Session = Depends(get_db)
):
    """Generate and store analytics data"""
    try:
        # Calculate period dates
        now = datetime.now()
        if period_type == "daily":
            period_start = now - timedelta(days=1)
        elif period_type == "weekly":
            period_start = now - timedelta(days=7)
        elif period_type == "monthly":
            period_start = now - timedelta(days=30)
        else:
            raise HTTPException(status_code=400, detail="Invalid period type")
        
        # Get predictions for the period
        predictions = db.query(Prediction).filter(
            Prediction.prediction_date >= period_start,
            Prediction.prediction_date <= now,
            Prediction.is_correct.isnot(None)
        ).all()
        
        if not predictions:
            return {"message": "No predictions found for the specified period"}
        
        # Calculate analytics
        total_predictions = len(predictions)
        correct_predictions = sum(1 for p in predictions if p.is_correct)
        accuracy_percentage = (correct_predictions / total_predictions) * 100
        
        # Confidence breakdown
        high_confidence = [p for p in predictions if p.confidence_score > 0.8]
        medium_confidence = [p for p in predictions if 0.6 <= p.confidence_score <= 0.8]
        low_confidence = [p for p in predictions if p.confidence_score < 0.6]
        
        high_confidence_accuracy = (sum(1 for p in high_confidence if p.is_correct) / len(high_confidence) * 100) if high_confidence else 0
        medium_confidence_accuracy = (sum(1 for p in medium_confidence if p.is_correct) / len(medium_confidence) * 100) if medium_confidence else 0
        low_confidence_accuracy = (sum(1 for p in low_confidence if p.is_correct) / len(low_confidence) * 100) if low_confidence else 0
        
        # Betting stats
        bets_recommended = [p for p in predictions if p.recommended_bet in ['home', 'away']]
        total_bets_recommended = len(bets_recommended)
        winning_bets = sum(1 for p in bets_recommended if p.is_correct)
        betting_roi = ((winning_bets / total_bets_recommended) - 0.5) * 100 if total_bets_recommended > 0 else 0
        
        # Create analytics record
        analytics = Analytics(
            period_type=period_type,
            period_start=period_start,
            period_end=now,
            total_predictions=total_predictions,
            correct_predictions=correct_predictions,
            accuracy_percentage=accuracy_percentage,
            high_confidence_accuracy=high_confidence_accuracy,
            medium_confidence_accuracy=medium_confidence_accuracy,
            low_confidence_accuracy=low_confidence_accuracy,
            total_bets_recommended=total_bets_recommended,
            winning_bets=winning_bets,
            betting_roi=betting_roi,
            model_version="1.0.0",
            average_confidence=sum(p.confidence_score for p in predictions) / total_predictions
        )
        
        db.add(analytics)
        db.commit()
        
        return {
            "message": f"Analytics generated for {period_type} period",
            "analytics_id": analytics.id,
            "accuracy_percentage": accuracy_percentage
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating analytics: {str(e)}") 