from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Database engine configuration with production-ready settings
def create_database_engine():
    """Create database engine with appropriate configuration"""
    
    # Base configuration
    engine_kwargs = {
        "echo": settings.debug,  # Log SQL queries in debug mode
        "pool_pre_ping": True,   # Verify connections before use
    }
    
    # SQLite-specific settings
    if "sqlite" in settings.database_url:
        engine_kwargs.update({
            "connect_args": {"check_same_thread": False},
            "poolclass": None,  # SQLite doesn't support connection pooling
        })
    else:
        # PostgreSQL/Production settings
        engine_kwargs.update({
            "poolclass": QueuePool,
            "pool_size": 20,           # Number of connections to maintain
            "max_overflow": 30,        # Additional connections when pool is full
            "pool_timeout": 30,        # Timeout for getting connection from pool
            "pool_recycle": 3600,      # Recycle connections after 1 hour
        })
    
    return create_engine(settings.database_url, **engine_kwargs)

# Create engine
engine = create_database_engine()

# Session configuration
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Prevent lazy loading issues
)

Base = declarative_base()

def get_db():
    """Database dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def test_database_connection():
    """Test database connectivity"""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False 