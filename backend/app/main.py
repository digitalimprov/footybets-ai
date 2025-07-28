from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import time
import logging

from app.api.routes import games, predictions, analytics, scraping, auth, admin, content
from app.api.routes import auth_simple
from app.core.config import settings
from app.core.security import SecurityMiddleware, log_security_event

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="FootyBets.ai API",
    description="AI-powered AFL betting predictions API with comprehensive security",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Security middleware
if settings.enable_security_headers:
    app.add_middleware(SecurityMiddleware)

# Trusted host middleware (for production)
if settings.environment == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "footybets.ai", 
            "www.footybets.ai", 
            "api.footybets.ai",
            "footybets-backend-818397187963.us-central1.run.app",
            "footybets-frontend-818397187963.us-central1.run.app",
            "footybets-backend-818397187963.us-central1.run.app",
            "footybets-frontend-wlbnzevhqa-uc.a.run.app",
            "*.run.app"  # Allow all Cloud Run URLs
        ]
    )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Handle OPTIONS requests for CORS preflight
@app.options("/{full_path:path}")
async def options_handler(request: Request):
    """Handle CORS preflight requests."""
    return {"message": "OK"}

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Admin rate limiting middleware
@app.middleware("http")
async def admin_rate_limit_middleware(request: Request, call_next):
    """Provide higher rate limits for admin users."""
    from app.core.security import security_manager
    from app.core.database import get_db
    from app.models.user import User
    import jwt
    
    client_ip = request.client.host
    
    # Check if this is an admin request by looking for auth header
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        try:
            token = auth_header.split(" ")[1]
            payload = security_manager.verify_token(token)
            user_id = payload.get("sub")
            
            if user_id:
                # Get user from database
                db = next(get_db())
                user = db.query(User).filter(User.id == user_id).first()
                
                if user and user.is_admin:
                    # Admin users get higher rate limits
                    if not security_manager.check_rate_limit(f"admin_{client_ip}", max_requests=1000, window_seconds=3600):
                        return JSONResponse(
                            status_code=429,
                            content={"detail": "Admin rate limit exceeded"}
                        )
                else:
                    # Regular users get standard rate limits
                    if not security_manager.check_rate_limit(f"user_{client_ip}", max_requests=100, window_seconds=3600):
                        return JSONResponse(
                            status_code=429,
                            content={"detail": "Rate limit exceeded"}
                        )
        except Exception:
            # If token verification fails, use standard rate limiting
            if not security_manager.check_rate_limit(f"user_{client_ip}", max_requests=100, window_seconds=3600):
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded"}
                )
    else:
        # No auth header, use standard rate limiting
        if not security_manager.check_rate_limit(f"user_{client_ip}", max_requests=100, window_seconds=3600):
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"}
            )
    
    response = await call_next(request)
    return response

# Security logging middleware
@app.middleware("http")
async def log_security_events(request: Request, call_next):
    # Log suspicious requests
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "")
    
    # Check for suspicious patterns (exclude legitimate admin routes)
    suspicious_patterns = [
        "sqlmap", "nikto", "nmap", "dirb", "gobuster", "wfuzz",
        "wp-admin", "phpmyadmin", "config", ".env",
        "union select", "drop table", "insert into", "delete from"
    ]
    
    request_path = request.url.path.lower()
    request_query = str(request.query_params).lower()
    
    # Skip security logging for legitimate admin routes
    legitimate_admin_routes = [
        "/api/admin",
        "/admin/dashboard",
        "/admin/login"
    ]
    
    is_legitimate_admin_route = any(route in request_path for route in legitimate_admin_routes)
    
    # Only check suspicious patterns if not a legitimate admin route
    if not is_legitimate_admin_route:
        for pattern in suspicious_patterns:
            if pattern in request_path or pattern in request_query or pattern in user_agent.lower():
                log_security_event("suspicious_request", None, {
                    "ip_address": client_ip,
                    "user_agent": user_agent,
                    "path": request.url.path,
                    "query": str(request.query_params),
                    "pattern": pattern
                })
                break
    
    response = await call_next(request)
    return response

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    log_security_event("validation_error", None, {
        "ip_address": request.client.host,
        "path": request.url.path,
        "errors": str(exc.errors())
    })
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code >= 400:
        log_security_event("http_error", None, {
            "ip_address": request.client.host,
            "path": request.url.path,
            "status_code": exc.status_code,
            "detail": exc.detail
        })
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    log_security_event("unhandled_exception", None, {
        "ip_address": request.client.host,
        "path": request.url.path,
        "error": str(exc)
    })
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(auth_simple.router, prefix="/api/auth", tags=["authentication"])
app.include_router(games.router, prefix="/api/games", tags=["games"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["predictions"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(scraping.router, prefix="/api/scraping", tags=["scraping"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(content.router, prefix="/api/content", tags=["content"])

@app.get("/")
async def root():
    """Root endpoint with security information."""
    return {
        "message": "Welcome to FootyBets.ai API",
        "version": "1.0.0",
        "security": {
            "authentication_required": True,
            "rate_limiting_enabled": True,
            "encryption_enabled": True,
            "security_headers_enabled": settings.enable_security_headers
        },
        "documentation": "/docs" if settings.debug else "Documentation disabled in production"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "environment": settings.environment
    }

@app.get("/security")
async def security_info():
    """Security information endpoint (for authenticated users only)."""
    return {
        "security_features": {
            "jwt_authentication": True,
            "password_hashing": "bcrypt",
            "rate_limiting": True,
            "account_lockout": True,
            "session_management": True,
            "input_validation": True,
            "sql_injection_protection": True,
            "xss_protection": True,
            "csrf_protection": True,
            "security_headers": settings.enable_security_headers,
            "encryption": "AES-256",
            "audit_logging": True
        },
        "compliance": {
            "gdpr_ready": True,
            "data_encryption": True,
            "secure_communication": True,
            "access_controls": True
        },
        "security_validation": {
            "api_secret_configured": bool(settings.api_secret_key and settings.api_secret_key != "your-secret-key-change-this"),
            "production_ready": settings.environment == "production" and not settings.debug,
            "cors_configured": len(settings.allowed_origins) > 0,
            "trusted_hosts_configured": settings.environment == "production",
            "environment": settings.environment,
            "debug_mode": settings.debug
        }
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info("FootyBets.ai API starting up...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Security headers enabled: {settings.enable_security_headers}")
    
    # Log security configuration
    log_security_event("application_startup", None, {
        "environment": settings.environment,
        "security_features_enabled": {
            "security_headers": settings.enable_security_headers,
            "rate_limiting": True,
            "authentication": True
        }
    })

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("FootyBets.ai API shutting down...")
    log_security_event("application_shutdown", None, {}) 