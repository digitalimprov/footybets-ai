from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class UserTip(Base):
    __tablename__ = "user_tips"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    game_id = Column(Integer, ForeignKey("games.id"), index=True)
    
    # User information (simplified for now)
    user_name = Column(String, index=True)
    user_email = Column(String, index=True)
    
    # Tip details
    predicted_winner_id = Column(Integer, ForeignKey("teams.id"), index=True)
    predicted_home_score = Column(Integer)
    predicted_away_score = Column(Integer)
    
    # User reasoning
    reasoning = Column(Text)
    
    # Tip metadata
    tip_date = Column(DateTime, default=datetime.utcnow)
    is_correct = Column(Boolean, nullable=True)  # Set after game completion
    
    # Relationships
    user = relationship("User", back_populates="user_tips", lazy="joined")
    game = relationship("Game", lazy="joined")
    predicted_winner = relationship("Team", lazy="joined")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 