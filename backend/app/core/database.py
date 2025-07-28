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
        # PostgreSQL/Production settings with enhanced security
        engine_kwargs.update({
            "poolclass": QueuePool,
            "pool_size": 20,           # Number of connections to maintain
            "max_overflow": 30,        # Additional connections when pool is full
            "pool_timeout": 30,        # Timeout for getting connection from pool
            "pool_recycle": 3600,      # Recycle connections after 1 hour
            "connect_args": {
                "sslmode": "require",  # Force SSL connection for security
                "application_name": "footybets-backend",
                "connect_timeout": 10,  # Connection timeout
                "options": "-c statement_timeout=30000"  # 30 second query timeout
            }
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
    """Test database connectivity with security checks"""
    try:
        with engine.connect() as conn:
            from sqlalchemy import text
            
            # Test basic connectivity
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
            
            # Test SSL connection (for PostgreSQL)
            if "postgresql" in settings.database_url:
                ssl_result = conn.execute(text("SHOW ssl"))
                ssl_status = ssl_result.fetchone()
                logger.info(f"SSL Status: {ssl_status}")
            
            # Test connection security
            security_result = conn.execute(text("SELECT current_user, current_database()"))
            security_info = security_result.fetchone()
            logger.info(f"Connected as: {security_info}")
            
        logger.info("Database connection successful with security checks")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

def get_database_info():
    """Get database connection information for security monitoring"""
    try:
        with engine.connect() as conn:
            from sqlalchemy import text
            
            info = {}
            
            # Get PostgreSQL version
            if "postgresql" in settings.database_url:
                version_result = conn.execute(text("SELECT version()"))
                info['version'] = version_result.fetchone()[0]
                
                # Get SSL status
                ssl_result = conn.execute(text("SHOW ssl"))
                info['ssl_enabled'] = ssl_result.fetchone()[0]
                
                # Get connection count
                conn_count_result = conn.execute(text("SELECT count(*) FROM pg_stat_activity"))
                info['active_connections'] = conn_count_result.fetchone()[0]
            
            return info
    except Exception as e:
        logger.error(f"Failed to get database info: {e}")
        return {"error": str(e)} 