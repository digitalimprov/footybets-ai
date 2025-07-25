from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    season = Column(Integer, index=True)
    round_number = Column(Integer, index=True)
    game_number = Column(Integer)
    
    # Teams
    home_team_id = Column(Integer, ForeignKey("teams.id"), index=True)
    away_team_id = Column(Integer, ForeignKey("teams.id"), index=True)
    
    # Game details
    venue = Column(String)
    game_date = Column(DateTime, index=True)
    is_finished = Column(Boolean, default=False)
    
    # Scores (for completed games)
    home_score = Column(Integer)
    away_score = Column(Integer)
    home_goals = Column(Integer)
    away_goals = Column(Integer)
    home_behinds = Column(Integer)
    away_behinds = Column(Integer)
    
    # Weather and conditions
    weather = Column(String)
    temperature = Column(Float)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_games")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_games")
    predictions = relationship("Prediction", back_populates="game") 