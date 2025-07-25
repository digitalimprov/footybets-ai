from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.scrapers.afl_scraper import AFLScraper
from app.models.game import Game
from app.models.team import Team
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class ScrapingResponse(BaseModel):
    message: str
    games_scraped: int
    teams_created: int
    season: Optional[int] = None
    duration_seconds: float

@router.post("/historical-data")
async def scrape_historical_data(
    background_tasks: BackgroundTasks,
    start_season: int = Query(2020, description="Starting season to scrape"),
    end_season: int = Query(2024, description="Ending season to scrape"),
    db: Session = Depends(get_db)
):
    """Scrape historical AFL data from afltables.com.au"""
    try:
        scraper = AFLScraper()
        total_games = 0
        total_teams = 0
        start_time = datetime.now()
        
        for season in range(start_season, end_season + 1):
            logger.info(f"Scraping season {season}")
            
            # Scrape season data
            games_data = scraper.get_season_data(season)
            
            if games_data:
                # Save to database
                scraper.save_games_to_db(db, games_data)
                total_games += len(games_data)
                
                # Count unique teams
                unique_teams = set()
                for game in games_data:
                    unique_teams.add(game['home_team'])
                    unique_teams.add(game['away_team'])
                total_teams = len(unique_teams)
        
        duration = (datetime.now() - start_time).total_seconds()
        
        return ScrapingResponse(
            message=f"Successfully scraped {total_games} games from {start_season} to {end_season}",
            games_scraped=total_games,
            teams_created=total_teams,
            season=f"{start_season}-{end_season}",
            duration_seconds=duration
        )
        
    except Exception as e:
        logger.error(f"Error scraping historical data: {e}")
        raise HTTPException(status_code=500, detail=f"Error scraping data: {str(e)}")

@router.post("/season")
async def scrape_season(
    season: int = Query(2024, description="Season to scrape"),
    db: Session = Depends(get_db)
):
    """Scrape a specific season"""
    try:
        scraper = AFLScraper()
        start_time = datetime.now()
        
        # Scrape season data
        games_data = scraper.get_season_data(season)
        
        if not games_data:
            return ScrapingResponse(
                message=f"No data found for season {season}",
                games_scraped=0,
                teams_created=0,
                season=season,
                duration_seconds=0
            )
        
        # Save to database
        scraper.save_games_to_db(db, games_data)
        
        duration = (datetime.now() - start_time).total_seconds()
        
        return ScrapingResponse(
            message=f"Successfully scraped {len(games_data)} games for season {season}",
            games_scraped=len(games_data),
            teams_created=0,  # Teams are created as needed
            season=season,
            duration_seconds=duration
        )
        
    except Exception as e:
        logger.error(f"Error scraping season {season}: {e}")
        raise HTTPException(status_code=500, detail=f"Error scraping season: {str(e)}")

@router.post("/upcoming-games")
async def scrape_upcoming_games(db: Session = Depends(get_db)):
    """Scrape upcoming games from AFL website"""
    try:
        scraper = AFLScraper()
        start_time = datetime.now()
        
        # Get upcoming games
        upcoming_games = scraper.get_upcoming_games()
        
        if not upcoming_games:
            return ScrapingResponse(
                message="No upcoming games found",
                games_scraped=0,
                teams_created=0,
                duration_seconds=0
            )
        
        # Save to database
        scraper.save_games_to_db(db, upcoming_games)
        
        duration = (datetime.now() - start_time).total_seconds()
        
        return ScrapingResponse(
            message=f"Successfully scraped {len(upcoming_games)} upcoming games",
            games_scraped=len(upcoming_games),
            teams_created=0,
            duration_seconds=duration
        )
        
    except Exception as e:
        logger.error(f"Error scraping upcoming games: {e}")
        raise HTTPException(status_code=500, detail=f"Error scraping upcoming games: {str(e)}")

@router.get("/status")
async def get_scraping_status(db: Session = Depends(get_db)):
    """Get current scraping status and data statistics"""
    try:
        # Get database statistics
        total_games = db.query(Game).count()
        total_teams = db.query(Team).count()
        
        # Get games by season
        season_stats = db.query(
            Game.season,
            db.func.count(Game.id).label('game_count')
        ).group_by(Game.season).order_by(Game.season.desc()).all()
        
        # Get recent scraping activity
        recent_games = db.query(Game).order_by(Game.created_at.desc()).limit(10).all()
        
        return {
            "total_games": total_games,
            "total_teams": total_teams,
            "seasons_available": [stat.season for stat in season_stats],
            "season_breakdown": [
                {"season": stat.season, "games": stat.game_count}
                for stat in season_stats
            ],
            "recent_games": [
                {
                    "id": game.id,
                    "home_team": game.home_team.name,
                    "away_team": game.away_team.name,
                    "date": game.game_date,
                    "created_at": game.created_at
                }
                for game in recent_games
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting scraping status: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")

@router.post("/cleanup")
async def cleanup_duplicate_data(db: Session = Depends(get_db)):
    """Clean up duplicate games and teams"""
    try:
        # Find and remove duplicate games
        duplicate_games = db.query(Game).filter(
            db.func.count(Game.id) > 1
        ).group_by(
            Game.season, Game.round_number, Game.game_number
        ).having(
            db.func.count(Game.id) > 1
        ).all()
        
        games_removed = 0
        for game in duplicate_games:
            db.delete(game)
            games_removed += 1
        
        # Find and remove duplicate teams
        duplicate_teams = db.query(Team).filter(
            db.func.count(Team.id) > 1
        ).group_by(Team.name).having(
            db.func.count(Team.id) > 1
        ).all()
        
        teams_removed = 0
        for team in duplicate_teams:
            db.delete(team)
            teams_removed += 1
        
        db.commit()
        
        return {
            "message": "Cleanup completed",
            "duplicate_games_removed": games_removed,
            "duplicate_teams_removed": teams_removed
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error during cleanup: {e}")
        raise HTTPException(status_code=500, detail=f"Error during cleanup: {str(e)}") 