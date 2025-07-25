from pydantic_settings import BaseSettings
from typing import Optional, List
import secrets

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/footybets"

    # Google Gemini API
    gemini_api_key: str

    # Scraping settings
    scraping_delay: int = 1
    user_agent: str = "Mozilla/5.0 (compatible; FootyBets/1.0)"

    # API settings
    api_secret_key: str = "your-secret-key-change-this"
    
    # Security settings
    secret_key: str = secrets.token_urlsafe(32)
    encryption_key: str = secrets.token_urlsafe(32)
    
    # JWT settings
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    
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
    
    # Email settings
    smtp_server: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    from_email: str = "noreply@footybets.ai"
    from_name: str = "FootyBets.ai"
    frontend_url: str = "https://footybets.ai"
    
    # CORS settings
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://footybets.ai",
        "https://www.footybets.ai"
    ]
    
    # Security headers
    enable_security_headers: bool = True
    enable_hsts: bool = True
    enable_csp: bool = True
    
    # Monitoring and logging
    enable_sentry: bool = False
    sentry_dsn: Optional[str] = None
    log_level: str = "INFO"
    
    # Redis (for rate limiting and caching)
    redis_url: Optional[str] = None
    
    # AFL Tables URL
    afl_tables_url: str = "https://afltables.com.au/afl"
    
    # Environment
    environment: str = "development"
    debug: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings() 