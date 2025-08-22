from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.scrapers.afltables_upcoming import AFLTablesUpcomingScraper
from app.scrapers.afltables_results import AFLTablesResultsScraper
from app.ai.predictor import AFLPredictor
from app.models.game import Game
from app.models.prediction import Prediction
import logging

logger = logging.getLogger(__name__)

class SchedulerService:
    """Service for managing automated tasks"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.is_running = False
        
    def start(self):
        """Start the scheduler"""
        if not self.is_running:
            self._setup_jobs()
            self.scheduler.start()
            self.is_running = True
            logger.info("Scheduler service started successfully")
    
    def stop(self):
        """Stop the scheduler"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("Scheduler service stopped")
    
    def _setup_jobs(self):
        """Setup all scheduled jobs"""
        
        # Weekly scraping of upcoming games - every Tuesday at 6:00 AM
        self.scheduler.add_job(
            func=self._scrape_upcoming_games,
            trigger=CronTrigger(day_of_week='tue', hour=6, minute=0),
            id='scrape_upcoming_games',
            name='Scrape Upcoming AFL Games',
            replace_existing=True
        )
        
        # Weekly scraping of results - every Monday at 8:00 AM
        self.scheduler.add_job(
            func=self._scrape_recent_results,
            trigger=CronTrigger(day_of_week='mon', hour=8, minute=0),
            id='scrape_recent_results',
            name='Scrape Recent AFL Results',
            replace_existing=True
        )
        
        # Generate tips for upcoming games - every Tuesday at 10:00 AM
        self.scheduler.add_job(
            func=self._generate_weekly_tips,
            trigger=CronTrigger(day_of_week='tue', hour=10, minute=0),
            id='generate_weekly_tips',
            name='Generate Weekly AFL Tips',
            replace_existing=True
        )
        
        # Update prediction accuracy - every Monday at 9:00 AM
        self.scheduler.add_job(
            func=self._update_prediction_accuracy,
            trigger=CronTrigger(day_of_week='mon', hour=9, minute=0),
            id='update_prediction_accuracy',
            name='Update Prediction Accuracy',
            replace_existing=True
        )
        
        # Daily health check - every day at 7:00 AM
        self.scheduler.add_job(
            func=self._daily_health_check,
            trigger=CronTrigger(hour=7, minute=0),
            id='daily_health_check',
            name='Daily System Health Check',
            replace_existing=True
        )
        
        logger.info("Scheduled jobs setup completed")
    
    def _scrape_upcoming_games(self):
        """Automated task to scrape upcoming AFL games"""
        logger.info("Starting automated scraping of upcoming games")
        
        db = SessionLocal()
        try:
            scraper = AFLTablesUpcomingScraper()
            
            # Get upcoming games for next 2 weeks
            upcoming_data = scraper.get_upcoming_games(weeks_ahead=2)
            
            if upcoming_data['success']:
                # Save to database
                result = scraper.save_upcoming_games_to_db(db, upcoming_data)
                
                if result['success']:
                    logger.info(f"Successfully processed {result['total_processed']} upcoming games. "
                              f"Saved: {result['saved_count']}, Updated: {result['updated_count']}")
                    
                    if result['errors']:
                        logger.warning(f"Encountered {len(result['errors'])} errors: {result['errors']}")
                else:
                    logger.error(f"Failed to save upcoming games: {result['error']}")
            else:
                logger.error(f"Failed to scrape upcoming games: {upcoming_data['error']}")
                
        except Exception as e:
            logger.error(f"Error in automated upcoming games scraping: {str(e)}")
        finally:
            db.close()
    
    def _scrape_recent_results(self):
        """Automated task to scrape recent AFL results"""
        logger.info("Starting automated scraping of recent results")
        
        db = SessionLocal()
        try:
            scraper = AFLTablesResultsScraper()
            
            # Get results from past week
            results_data = scraper.get_recent_results(weeks_back=1)
            
            if results_data['success']:
                # Save to database
                result = scraper.save_results_to_db(db, results_data)
                
                if result['success']:
                    logger.info(f"Successfully processed {result['total_processed']} recent results. "
                              f"Updated: {result['updated_count']}")
                    
                    if result['errors']:
                        logger.warning(f"Encountered {len(result['errors'])} errors: {result['errors']}")
                else:
                    logger.error(f"Failed to save recent results: {result['error']}")
            else:
                logger.error(f"Failed to scrape recent results: {results_data['error']}")
                
        except Exception as e:
            logger.error(f"Error in automated results scraping: {str(e)}")
        finally:
            db.close()
    
    def _generate_weekly_tips(self):
        """Automated task to generate tips for upcoming games"""
        logger.info("Starting automated weekly tip generation")
        
        db = SessionLocal()
        try:
            predictor = AFLPredictor()
            
            # Get upcoming games for this week
            one_week_ahead = datetime.now() + timedelta(weeks=1)
            upcoming_games = db.query(Game).filter(
                Game.is_finished == False,
                Game.game_date > datetime.now(),
                Game.game_date <= one_week_ahead
            ).all()
            
            if not upcoming_games:
                logger.info("No upcoming games found for tip generation")
                return
            
            # Generate predictions for upcoming games
            predictions = predictor.generate_predictions(db, upcoming_games)
            
            # Save predictions to database
            predictions_saved = 0
            for prediction in predictions:
                # Check if prediction already exists
                existing = db.query(Prediction).filter(
                    Prediction.game_id == prediction.game_id,
                    Prediction.model_version == prediction.model_version
                ).first()
                
                if not existing:
                    db.add(prediction)
                    predictions_saved += 1
            
            db.commit()
            
            logger.info(f"Generated and saved {predictions_saved} new predictions for {len(upcoming_games)} upcoming games")
            
        except Exception as e:
            logger.error(f"Error in automated tip generation: {str(e)}")
            db.rollback()
        finally:
            db.close()
    
    def _update_prediction_accuracy(self):
        """Automated task to update prediction accuracy"""
        logger.info("Starting automated prediction accuracy update")
        
        db = SessionLocal()
        try:
            scraper = AFLTablesResultsScraper()
            result = scraper.update_prediction_accuracy(db)
            
            if result['success']:
                logger.info(f"Updated accuracy for {result['updated_predictions']} predictions "
                          f"across {result['games_processed']} games")
            else:
                logger.error(f"Failed to update prediction accuracy: {result['error']}")
                
        except Exception as e:
            logger.error(f"Error in automated prediction accuracy update: {str(e)}")
        finally:
            db.close()
    
    def _daily_health_check(self):
        """Daily health check of the system"""
        logger.info("Performing daily health check")
        
        db = SessionLocal()
        try:
            # Check database connectivity
            game_count = db.query(Game).count()
            prediction_count = db.query(Prediction).count()
            
            # Check for recent data
            recent_games = db.query(Game).filter(
                Game.game_date >= datetime.now() - timedelta(days=7)
            ).count()
            
            recent_predictions = db.query(Prediction).filter(
                Prediction.prediction_date >= datetime.now() - timedelta(days=7)
            ).count()
            
            logger.info(f"Health check: {game_count} total games, {prediction_count} total predictions")
            logger.info(f"Recent activity: {recent_games} games, {recent_predictions} predictions in past 7 days")
            
            # Check scheduler status
            jobs = self.scheduler.get_jobs()
            logger.info(f"Scheduler health: {len(jobs)} jobs active")
            
            for job in jobs:
                next_run = job.next_run_time
                logger.info(f"  {job.name}: next run at {next_run}")
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
        finally:
            db.close()
    
    def run_job_now(self, job_id: str) -> dict:
        """Manually trigger a scheduled job"""
        try:
            job = self.scheduler.get_job(job_id)
            if not job:
                return {'success': False, 'error': f'Job {job_id} not found'}
            
            # Execute the job function
            if job_id == 'scrape_upcoming_games':
                self._scrape_upcoming_games()
            elif job_id == 'scrape_recent_results':
                self._scrape_recent_results()
            elif job_id == 'generate_weekly_tips':
                self._generate_weekly_tips()
            elif job_id == 'update_prediction_accuracy':
                self._update_prediction_accuracy()
            elif job_id == 'daily_health_check':
                self._daily_health_check()
            else:
                return {'success': False, 'error': f'Unknown job: {job_id}'}
            
            return {'success': True, 'message': f'Job {job_id} executed successfully'}
            
        except Exception as e:
            logger.error(f"Error running job {job_id}: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_job_status(self) -> dict:
        """Get status of all scheduled jobs"""
        try:
            jobs = []
            for job in self.scheduler.get_jobs():
                jobs.append({
                    'id': job.id,
                    'name': job.name,
                    'next_run': job.next_run_time.isoformat() if job.next_run_time else None,
                    'trigger': str(job.trigger)
                })
            
            return {
                'success': True,
                'scheduler_running': self.is_running,
                'jobs': jobs,
                'total_jobs': len(jobs)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# Global scheduler instance
scheduler_service = SchedulerService() 