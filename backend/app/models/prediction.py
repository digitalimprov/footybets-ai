from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), index=True)
    
    # Prediction details
    predicted_winner_id = Column(Integer, ForeignKey("teams.id"), index=True)
    confidence_score = Column(Float)  # 0.0 to 1.0
    predicted_home_score = Column(Integer)
    predicted_away_score = Column(Integer)
    
    # AI reasoning
    reasoning = Column(Text)
    factors_considered = Column(Text)  # JSON string of factors
    
    # Betting recommendations
    recommended_bet = Column(String)  # "home", "away", "draw", "none"
    bet_confidence = Column(Float)  # 0.0 to 1.0
    odds_analysis = Column(Text)  # JSON string of odds analysis
    
    # Prediction metadata
    model_version = Column(String)
    prediction_date = Column(DateTime, default=datetime.utcnow)
    is_correct = Column(Boolean, nullable=True)  # Set after game completion
    
    # Relationships
    game = relationship("Game", back_populates="predictions")
    predicted_winner = relationship("Team")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 