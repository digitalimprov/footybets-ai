from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from datetime import datetime
from app.core.database import Base

class Analytics(Base):
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Analytics period
    period_type = Column(String)  # "daily", "weekly", "monthly", "season"
    period_start = Column(DateTime, index=True)
    period_end = Column(DateTime, index=True)
    
    # Prediction accuracy
    total_predictions = Column(Integer)
    correct_predictions = Column(Integer)
    accuracy_percentage = Column(Float)
    
    # Performance by confidence level
    high_confidence_accuracy = Column(Float)  # > 0.8
    medium_confidence_accuracy = Column(Float)  # 0.6-0.8
    low_confidence_accuracy = Column(Float)  # < 0.6
    
    # Team performance
    team_performance_data = Column(Text)  # JSON string of team-specific stats
    
    # Betting performance
    total_bets_recommended = Column(Integer)
    winning_bets = Column(Integer)
    betting_roi = Column(Float)
    
    # Model performance
    model_version = Column(String)
    average_confidence = Column(Float)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 