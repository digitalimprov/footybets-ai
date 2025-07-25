from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic info
    name = Column(String, index=True)
    afl_id = Column(String, unique=True, index=True)  # AFL Tables player ID
    date_of_birth = Column(Date)
    height = Column(Integer)  # in cm
    weight = Column(Integer)  # in kg
    position = Column(String)
    
    # Team info
    current_team_id = Column(Integer, ForeignKey("teams.id"), index=True)
    
    # Career stats
    games_played = Column(Integer, default=0)
    goals_kicked = Column(Integer, default=0)
    behinds_kicked = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    current_team = relationship("Team", back_populates="players")
    player_stats = relationship("PlayerGameStats", back_populates="player")

class PlayerGameStats(Base):
    __tablename__ = "player_game_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Game and player
    game_id = Column(Integer, ForeignKey("games.id"), index=True)
    player_id = Column(Integer, ForeignKey("players.id"), index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), index=True)
    
    # Playing stats
    goals = Column(Integer, default=0)
    behinds = Column(Integer, default=0)
    kicks = Column(Integer, default=0)
    handballs = Column(Integer, default=0)
    marks = Column(Integer, default=0)
    tackles = Column(Integer, default=0)
    hitouts = Column(Integer, default=0)
    frees_for = Column(Integer, default=0)
    frees_against = Column(Integer, default=0)
    
    # Advanced stats
    disposals = Column(Integer, default=0)  # kicks + handballs
    contested_possessions = Column(Integer, default=0)
    uncontested_possessions = Column(Integer, default=0)
    inside_50s = Column(Integer, default=0)
    rebound_50s = Column(Integer, default=0)
    clearances = Column(Integer, default=0)
    clangers = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    game = relationship("Game", back_populates="player_stats")
    player = relationship("Player", back_populates="player_stats")
    team = relationship("Team") 