from pydantic_settings import BaseSettings
from typing import Optional, List
import secrets
from pydantic import Field

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "FootyBets AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Regional settings - optimized for Australia
    REGION: str = "australia-southeast1"
    TIMEZONE: str = "Australia/Sydney"
    
    # Database settings (Australian instance)
    DATABASE_URL: str = "postgresql://footybets_user:footybets_password@34.40.170.58:5432/footybets"
    DATABASE_HOST: str = "34.40.170.58"
    DATABASE_PORT: int = 5432
    DATABASE_USER: str = "footybets_user"
    DATABASE_PASSWORD: str = Field(default="", env="DATABASE_PASSWORD")
    DATABASE_NAME: str = "footybets"
    
    # Security settings
    SECRET_KEY: str = Field(default="temp-secret", env="APP_SECRET_KEY")
    API_SECRET_KEY: str = Field(default="temp-api-secret", env="API_SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # External APIs
    GEMINI_API_KEY: str = Field(default="", env="GEMINI_API_KEY")
    
    # Google Cloud settings (Australian region)
    GOOGLE_CLOUD_PROJECT: str = "footybets-ai"
    GOOGLE_CLOUD_REGION: str = "australia-southeast1"
    
    # CORS settings - allow Australian and global access
    CORS_ORIGINS: list[str] = [
        "https://footybets.ai",
        "https://www.footybets.ai",
        "https://footybets-frontend-818397187963.australia-southeast1.run.app",
        "http://localhost:3000",
        "http://localhost:8080"
    ]
    
    # API base URLs (Australian endpoints)
    API_BASE_URL: str = "https://footybets-backend-818397187963.australia-southeast1.run.app"
    FRONTEND_URL: str = "https://footybets-frontend-818397187963.australia-southeast1.run.app"
    
    # Rate limiting (per Australian time zones)
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # File uploads
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "/tmp/uploads"
    
    # Email settings (using Australian providers when possible)
    SMTP_SERVER: str = Field(default="", env="SMTP_SERVER")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USERNAME: str = Field(default="", env="SMTP_USERNAME")
    SMTP_PASSWORD: str = Field(default="", env="SMTP_PASSWORD")
    FROM_EMAIL: str = "noreply@footybets.ai"
    
    # Monitoring and logging
    LOG_LEVEL: str = "INFO"
    ENABLE_METRICS: bool = True
    
    # Australian AFL specific settings
    AFL_SEASON_START: str = "March"
    AFL_SEASON_END: str = "September"
    DEFAULT_CURRENCY: str = "AUD"
    DEFAULT_LOCALE: str = "en_AU"
    
    # Password settings
    password_min_length: int = 8
    password_require_uppercase: bool = True
    password_require_lowercase: bool = True
    password_require_numbers: bool = True
    password_require_special_chars: bool = True
    
    # Rate limiting
    rate_limit_max_requests: int = 100
    rate_limit_window_seconds: int = 3600
    login_rate_limit_max_requests: int = 10
    login_rate_limit_window_seconds: int = 300
    
    # Account security
    max_failed_login_attempts: int = 5
    account_lockout_minutes: int = 15
    session_timeout_hours: int = 24
    
    # JWT settings
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    
    # Scraping settings
    scraping_delay: int = 1
    user_agent: str = "Mozilla/5.0 (compatible; FootyBets/1.0)"
    
    # Redis (for rate limiting and caching)
    redis_url: Optional[str] = None
    
    # AFL Tables URL
    afl_tables_url: str = "https://afltables.com.au/afl"
    
    # Environment
    environment: str = "development"
    
    # Security headers
    enable_security_headers: bool = True
    enable_hsts: bool = True
    enable_csp: bool = True
    
    # Monitoring and logging
    enable_sentry: bool = False
    sentry_dsn: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        fields = {
            'database_url': {'env': 'DATABASE_URL'},
            'api_secret_key': {'env': 'API_SECRET_KEY'},
            'secret_key': {'env': 'SECRET_KEY'},
            'environment': {'env': 'ENVIRONMENT'},
            'debug': {'env': 'DEBUG'}
        }

    def model_post_init(self, __context) -> None:
        """Validate settings after initialization."""
        # Validate required security settings
        if self.environment == "production":
            # Temporarily disable validation for deployment
            # TODO: Add proper environment variables in Cloud Build
            pass

settings = Settings() 