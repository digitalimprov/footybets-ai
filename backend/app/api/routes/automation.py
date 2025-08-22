from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.scrapers.afltables_upcoming import AFLTablesUpcomingScraper
from app.scrapers.afltables_results import AFLTablesResultsScraper
from app.services.scheduler_service import scheduler_service
from pydantic import BaseModel

router = APIRouter()

class ScrapingResponse(BaseModel):
    success: bool
    message: str
    games_processed: Optional[int] = None
    errors: Optional[List[str]] = None
    data: Optional[dict] = None

class SchedulerStatusResponse(BaseModel):
    success: bool
    scheduler_running: bool
    jobs: List[dict]
    total_jobs: int

@router.get("/scraping/upcoming", response_model=ScrapingResponse)
async def scrape_upcoming_games(
    weeks_ahead: int = Query(2, description="Number of weeks ahead to scrape"),
    save_to_db: bool = Query(True, description="Whether to save results to database"),
    db: Session = Depends(get_db)
):
    """Manually trigger scraping of upcoming AFL games"""
    try:
        scraper = AFLTablesUpcomingScraper()
        
        # Scrape upcoming games
        upcoming_data = scraper.get_upcoming_games(weeks_ahead=weeks_ahead)
        
        if not upcoming_data['success']:
            raise HTTPException(status_code=500, detail=f"Scraping failed: {upcoming_data['error']}")
        
        result = {
            'success': True,
            'message': f"Found {upcoming_data['total_games']} upcoming games",
            'games_processed': upcoming_data['total_games'],
            'data': {
                'date_range': upcoming_data['date_range'],
                'games': upcoming_data['games'][:10] if len(upcoming_data['games']) > 10 else upcoming_data['games']  # Limit response size
            }
        }
        
        # Save to database if requested
        if save_to_db:
            save_result = scraper.save_upcoming_games_to_db(db, upcoming_data)
            
            if save_result['success']:
                result['message'] += f". Saved {save_result['saved_count']} new games, updated {save_result['updated_count']} existing games"
                if save_result['errors']:
                    result['errors'] = save_result['errors']
            else:
                raise HTTPException(status_code=500, detail=f"Database save failed: {save_result['error']}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping upcoming games: {str(e)}")

@router.get("/scraping/results", response_model=ScrapingResponse)
async def scrape_recent_results(
    weeks_back: int = Query(1, description="Number of weeks back to scrape results"),
    save_to_db: bool = Query(True, description="Whether to save results to database"),
    db: Session = Depends(get_db)
):
    """Manually trigger scraping of recent AFL results"""
    try:
        scraper = AFLTablesResultsScraper()
        
        # Scrape recent results
        results_data = scraper.get_recent_results(weeks_back=weeks_back)
        
        if not results_data['success']:
            raise HTTPException(status_code=500, detail=f"Scraping failed: {results_data['error']}")
        
        result = {
            'success': True,
            'message': f"Found {results_data['total_games']} completed games",
            'games_processed': results_data['total_games'],
            'data': {
                'date_range': results_data['date_range'],
                'games': results_data['games'][:10] if len(results_data['games']) > 10 else results_data['games']  # Limit response size
            }
        }
        
        # Save to database if requested
        if save_to_db:
            save_result = scraper.save_results_to_db(db, results_data)
            
            if save_result['success']:
                result['message'] += f". Updated {save_result['updated_count']} games with results"
                if save_result['errors']:
                    result['errors'] = save_result['errors']
            else:
                raise HTTPException(status_code=500, detail=f"Database save failed: {save_result['error']}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping recent results: {str(e)}")

@router.post("/scraping/update-accuracy", response_model=ScrapingResponse)
async def update_prediction_accuracy(db: Session = Depends(get_db)):
    """Update prediction accuracy for recently completed games"""
    try:
        scraper = AFLTablesResultsScraper()
        result = scraper.update_prediction_accuracy(db)
        
        if result['success']:
            return ScrapingResponse(
                success=True,
                message=f"Updated accuracy for {result['updated_predictions']} predictions across {result['games_processed']} games",
                games_processed=result['games_processed'],
                data={'updated_predictions': result['updated_predictions']}
            )
        else:
            raise HTTPException(status_code=500, detail=f"Failed to update accuracy: {result['error']}")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating prediction accuracy: {str(e)}")

@router.get("/scheduler/status", response_model=SchedulerStatusResponse)
async def get_scheduler_status():
    """Get the status of the automated scheduler"""
    try:
        status = scheduler_service.get_job_status()
        
        if status['success']:
            return SchedulerStatusResponse(**status)
        else:
            raise HTTPException(status_code=500, detail=f"Failed to get scheduler status: {status['error']}")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting scheduler status: {str(e)}")

@router.post("/scheduler/start")
async def start_scheduler():
    """Start the automated scheduler"""
    try:
        scheduler_service.start()
        return {"success": True, "message": "Scheduler started successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting scheduler: {str(e)}")

@router.post("/scheduler/stop")
async def stop_scheduler():
    """Stop the automated scheduler"""
    try:
        scheduler_service.stop()
        return {"success": True, "message": "Scheduler stopped successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error stopping scheduler: {str(e)}")

@router.post("/scheduler/run-job/{job_id}")
async def run_job_now(job_id: str):
    """Manually trigger a specific scheduled job"""
    try:
        valid_jobs = [
            'scrape_upcoming_games',
            'scrape_recent_results', 
            'generate_weekly_tips',
            'update_prediction_accuracy',
            'daily_health_check'
        ]
        
        if job_id not in valid_jobs:
            raise HTTPException(status_code=400, detail=f"Invalid job ID. Valid jobs: {', '.join(valid_jobs)}")
        
        result = scheduler_service.run_job_now(job_id)
        
        if result['success']:
            return result
        else:
            raise HTTPException(status_code=500, detail=result['error'])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running job: {str(e)}")

@router.get("/scraping/current-round")
async def get_current_round():
    """Get the current AFL round number"""
    try:
        scraper = AFLTablesUpcomingScraper()
        current_round = scraper.get_current_round()
        
        if current_round:
            return {
                "success": True,
                "current_round": current_round,
                "message": f"Current AFL round is {current_round}"
            }
        else:
            return {
                "success": False,
                "message": "Could not determine current round"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting current round: {str(e)}")

@router.post("/automation/full-weekly-update")
async def run_full_weekly_update(db: Session = Depends(get_db)):
    """Run a complete weekly update: scrape results, scrape upcoming games, and generate tips"""
    try:
        results = {
            'steps_completed': [],
            'errors': [],
            'success': True
        }
        
        # Step 1: Scrape recent results
        try:
            scraper_results = AFLTablesResultsScraper()
            results_data = scraper_results.get_recent_results(weeks_back=1)
            
            if results_data['success']:
                save_result = scraper_results.save_results_to_db(db, results_data)
                if save_result['success']:
                    results['steps_completed'].append(f"Updated {save_result['updated_count']} recent results")
                else:
                    results['errors'].append(f"Failed to save results: {save_result['error']}")
            else:
                results['errors'].append(f"Failed to scrape results: {results_data['error']}")
                
        except Exception as e:
            results['errors'].append(f"Error in results scraping: {str(e)}")
        
        # Step 2: Update prediction accuracy
        try:
            accuracy_result = scraper_results.update_prediction_accuracy(db)
            if accuracy_result['success']:
                results['steps_completed'].append(f"Updated accuracy for {accuracy_result['updated_predictions']} predictions")
            else:
                results['errors'].append(f"Failed to update accuracy: {accuracy_result['error']}")
        except Exception as e:
            results['errors'].append(f"Error updating accuracy: {str(e)}")
        
        # Step 3: Scrape upcoming games
        try:
            scraper_upcoming = AFLTablesUpcomingScraper()
            upcoming_data = scraper_upcoming.get_upcoming_games(weeks_ahead=2)
            
            if upcoming_data['success']:
                save_result = scraper_upcoming.save_upcoming_games_to_db(db, upcoming_data)
                if save_result['success']:
                    results['steps_completed'].append(f"Processed {save_result['total_processed']} upcoming games")
                else:
                    results['errors'].append(f"Failed to save upcoming games: {save_result['error']}")
            else:
                results['errors'].append(f"Failed to scrape upcoming games: {upcoming_data['error']}")
                
        except Exception as e:
            results['errors'].append(f"Error in upcoming games scraping: {str(e)}")
        
        # Step 4: Generate tips for upcoming games
        try:
            from app.ai.predictor import AFLPredictor
            from app.models.game import Game
            from app.models.prediction import Prediction
            
            predictor = AFLPredictor()
            
            # Get upcoming games for this week
            one_week_ahead = datetime.now() + timedelta(weeks=1)
            upcoming_games = db.query(Game).filter(
                Game.is_finished == False,
                Game.game_date > datetime.now(),
                Game.game_date <= one_week_ahead
            ).all()
            
            if upcoming_games:
                predictions = predictor.generate_predictions(db, upcoming_games)
                
                predictions_saved = 0
                for prediction in predictions:
                    existing = db.query(Prediction).filter(
                        Prediction.game_id == prediction.game_id,
                        Prediction.model_version == prediction.model_version
                    ).first()
                    
                    if not existing:
                        db.add(prediction)
                        predictions_saved += 1
                
                db.commit()
                results['steps_completed'].append(f"Generated {predictions_saved} new predictions")
            else:
                results['steps_completed'].append("No upcoming games found for tip generation")
                
        except Exception as e:
            results['errors'].append(f"Error generating tips: {str(e)}")
            db.rollback()
        
        # Determine overall success
        if results['errors']:
            results['success'] = False
        
        return {
            "success": results['success'],
            "message": f"Weekly update completed. {len(results['steps_completed'])} steps successful, {len(results['errors'])} errors",
            "steps_completed": results['steps_completed'],
            "errors": results['errors'] if results['errors'] else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in full weekly update: {str(e)}") 