from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.game import Game
from app.models.team import Team
from pydantic import BaseModel

router = APIRouter()

class GameResponse(BaseModel):
    id: int
    season: int
    round_number: int
    game_number: int
    home_team_name: str
    away_team_name: str
    venue: str
    game_date: datetime
    is_finished: bool
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    home_goals: Optional[int] = None
    away_goals: Optional[int] = None
    home_behinds: Optional[int] = None
    away_behinds: Optional[int] = None
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[GameResponse])
async def get_games(
    season: Optional[int] = Query(None, description="Filter by season"),
    round_number: Optional[int] = Query(None, description="Filter by round number"),
    upcoming: bool = Query(False, description="Get only upcoming games"),
    limit: int = Query(50, description="Number of games to return"),
    db: Session = Depends(get_db)
):
    """Get games with optional filtering"""
    query = db.query(Game).join(Team, Game.home_team_id == Team.id).join(
        Team, Game.away_team_id == Team.id
    )
    
    if season:
        query = query.filter(Game.season == season)
    
    if round_number:
        query = query.filter(Game.round_number == round_number)
    
    if upcoming:
        query = query.filter(
            Game.is_finished == False,
            Game.game_date > datetime.now()
        )
    
    games = query.order_by(Game.game_date.desc()).limit(limit).all()
    
    # Convert to response format
    response_games = []
    for game in games:
        response_games.append(GameResponse(
            id=game.id,
            season=game.season,
            round_number=game.round_number,
            game_number=game.game_number,
            home_team_name=game.home_team.name,
            away_team_name=game.away_team.name,
            venue=game.venue,
            game_date=game.game_date,
            is_finished=game.is_finished,
            home_score=game.home_score,
            away_score=game.away_score,
            home_goals=game.home_goals,
            away_goals=game.away_goals,
            home_behinds=game.home_behinds,
            away_behinds=game.away_behinds
        ))
    
    return response_games

@router.get("/upcoming", response_model=List[GameResponse])
async def get_upcoming_games(
    days: int = Query(7, description="Number of days ahead to look"),
    db: Session = Depends(get_db)
):
    """Get upcoming games in the next N days"""
    future_date = datetime.now() + timedelta(days=days)
    
    games = db.query(Game).filter(
        Game.is_finished == False,
        Game.game_date > datetime.now(),
        Game.game_date <= future_date
    ).order_by(Game.game_date.asc()).all()
    
    response_games = []
    for game in games:
        response_games.append(GameResponse(
            id=game.id,
            season=game.season,
            round_number=game.round_number,
            game_number=game.game_number,
            home_team_name=game.home_team.name,
            away_team_name=game.away_team.name,
            venue=game.venue,
            game_date=game.game_date,
            is_finished=game.is_finished,
            home_score=game.home_score,
            away_score=game.away_score,
            home_goals=game.home_goals,
            away_goals=game.away_goals,
            home_behinds=game.home_behinds,
            away_behinds=game.away_behinds
        ))
    
    return response_games

@router.get("/{game_id}", response_model=GameResponse)
async def get_game(game_id: int, db: Session = Depends(get_db)):
    """Get a specific game by ID"""
    game = db.query(Game).filter(Game.id == game_id).first()
    
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return GameResponse(
        id=game.id,
        season=game.season,
        round_number=game.round_number,
        game_number=game.game_number,
        home_team_name=game.home_team.name,
        away_team_name=game.away_team.name,
        venue=game.venue,
        game_date=game.game_date,
        is_finished=game.is_finished,
        home_score=game.home_score,
        away_score=game.away_score,
        home_goals=game.home_goals,
        away_goals=game.away_goals,
        home_behinds=game.home_behinds,
        away_behinds=game.away_behinds
    ) 