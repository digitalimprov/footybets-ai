import os
import secrets
import hashlib
import hmac
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import logging

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_REFRESH_TOKEN_EXPIRE_DAYS = 7

# Security headers
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
}

def validate_password_strength(password: str) -> bool:
    """Validate password meets security requirements"""
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'[0-9]', password):
        errors.append("Password must contain at least one number")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character")
    
    # Check for common weak passwords
    weak_passwords = [
        'password', '123456', 'qwerty', 'admin', 'footybets',
        'football', 'afl', 'betting', 'predictions'
    ]
    if password.lower() in weak_passwords:
        errors.append("Password cannot be a common weak password")
    
    # Check for repeated characters
    if re.search(r'(.)\1{2,}', password):
        errors.append("Password cannot contain more than 2 repeated characters")
    
    if errors:
        raise ValueError("; ".join(errors))
    
    return True

class SecurityManager:
    """Centralized security management for the application."""
    
    def __init__(self):
        # Generate a proper Fernet key if not provided
        if not hasattr(settings, 'encryption_key') or not settings.encryption_key:
            self.encryption_key = Fernet.generate_key()
        else:
            # Ensure the key is properly formatted for Fernet
            try:
                # Try to use the existing key
                self.encryption_key = settings.encryption_key.encode() if isinstance(settings.encryption_key, str) else settings.encryption_key
                # Test if it's valid by creating a Fernet instance
                Fernet(self.encryption_key)
            except (ValueError, TypeError):
                # If invalid, generate a new one
                self.encryption_key = Fernet.generate_key()
        
        self.cipher_suite = Fernet(self.encryption_key)
        
        # Rate limiting storage (in production, use Redis)
        self.rate_limit_store = {}
        
        # Failed login attempts tracking
        self.failed_attempts = {}
        
        # Session management
        self.active_sessions = {}
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    def generate_secure_token(self, length: int = 32) -> str:
        """Generate a cryptographically secure token."""
        return secrets.token_urlsafe(length)
    
    def create_user_with_secure_password(self, db: Session, user_data: dict) -> User:
        """Create user with password validation"""
        # Validate password strength
        validate_password_strength(user_data['password'])
        
        # Hash password
        hashed_password = self.hash_password(user_data['password'])
        
        # Create user
        user = User(
            email=user_data['email'],
            username=user_data['username'],
            hashed_password=hashed_password,
            is_active=True,
            is_verified=False,
            roles=["user"],
            permissions=["read:own", "write:own"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Log security event
        self.log_security_event(
            user_id=user.id,
            action="user_created",
            details=f"User {user.email} created with secure password",
            ip_address=user_data.get('ip_address', 'unknown')
        )
        
        return user
    
    def change_password_with_validation(self, db: Session, user: User, new_password: str, current_password: str) -> bool:
        """Change user password with validation"""
        # Verify current password
        if not self.verify_password(current_password, user.hashed_password):
            raise ValueError("Current password is incorrect")
        
        # Validate new password strength
        validate_password_strength(new_password)
        
        # Check if new password is same as old password
        if self.verify_password(new_password, user.hashed_password):
            raise ValueError("New password must be different from current password")
        
        # Hash new password
        new_hashed_password = self.hash_password(new_password)
        
        # Update user
        user.hashed_password = new_hashed_password
        user.last_password_change = datetime.utcnow()
        user.updated_at = datetime.utcnow()
        
        db.commit()
        
        # Log security event
        self.log_security_event(
            user_id=user.id,
            action="password_changed",
            details="Password changed successfully",
            ip_address="system"
        )
        
        return True
    
    def log_security_event(self, user_id: int, action: str, details: str, ip_address: str):
        """Log security events for audit purposes"""
        try:
            from app.models.security_log import SecurityLog
            
            security_log = SecurityLog(
                user_id=user_id,
                action=action,
                details=details,
                ip_address=ip_address,
                created_at=datetime.utcnow()
            )
            
            # This would typically be done in a database session
            # For now, we'll just log it
            logger.info(f"Security Event: {action} - {details} - User: {user_id} - IP: {ip_address}")
            
        except Exception as e:
            logger.error(f"Failed to log security event: {e}")
    
    def check_rate_limit(self, identifier: str, max_requests: int = 10, window_seconds: int = 300) -> bool:
        """Check if request is within rate limits"""
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window_seconds)
        
        # Clean old entries
        if identifier in self.rate_limit_store:
            self.rate_limit_store[identifier] = [
                timestamp for timestamp in self.rate_limit_store[identifier]
                if timestamp > window_start
            ]
        else:
            self.rate_limit_store[identifier] = []
        
        # Check if limit exceeded
        if len(self.rate_limit_store[identifier]) >= max_requests:
            return False
        
        # Add current request
        self.rate_limit_store[identifier].append(now)
        return True
    
    def check_failed_login_attempts(self, identifier: str, max_attempts: int = 5) -> bool:
        """Check if user is locked due to failed login attempts"""
        now = datetime.utcnow()
        
        if identifier in self.failed_attempts:
            attempts = self.failed_attempts[identifier]
            # Clean old attempts
            attempts = [timestamp for timestamp in attempts if timestamp > now - timedelta(minutes=15)]
            self.failed_attempts[identifier] = attempts
            
            if len(attempts) >= max_attempts:
                return False
        
        return True
    
    def record_failed_login(self, identifier: str):
        """Record a failed login attempt"""
        now = datetime.utcnow()
        
        if identifier not in self.failed_attempts:
            self.failed_attempts[identifier] = []
        
        self.failed_attempts[identifier].append(now)
        
        # Log security event
        self.log_security_event(
            user_id=0,  # Unknown user
            action="failed_login",
            details=f"Failed login attempt for {identifier}",
            ip_address=identifier
        )
    
    def clear_failed_attempts(self, identifier: str):
        """Clear failed login attempts for successful login"""
        if identifier in self.failed_attempts:
            del self.failed_attempts[identifier]
    
    def is_account_locked(self, identifier: str) -> bool:
        """Check if an account is locked due to failed login attempts"""
        return not self.check_failed_login_attempts(identifier)
    
    def track_failed_login(self, identifier: str):
        """Track a failed login attempt"""
        self.record_failed_login(identifier)
    
    def validate_password_strength(self, password: str) -> dict:
        """Validate password meets security requirements"""
        try:
            validate_password_strength(password)
            return {"valid": True, "errors": []}
        except ValueError as e:
            return {"valid": False, "errors": [str(e)]}
    
    def generate_api_key(self) -> str:
        """Generate a new API key."""
        return self.generate_secure_token(32)
    
    def hash_api_key(self, api_key: str) -> str:
        """Hash an API key for storage."""
        return self.hash_password(api_key)
    
    def create_session(self, user_id: int, session_data: Dict[str, Any] = None) -> str:
        """Create a new user session."""
        session_id = self.generate_secure_token()
        self.active_sessions[session_id] = {
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "data": session_data or {}
        }
        return session_id
    
    def validate_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Validate and return session data."""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        # Check if session has expired (24 hours)
        if (datetime.utcnow() - session["created_at"]).total_seconds() > 86400:
            del self.active_sessions[session_id]
            return None
        
        # Update last activity
        session["last_activity"] = datetime.utcnow()
        return session
    
    def invalidate_session(self, session_id: str):
        """Invalidate a user session."""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=JWT_ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT refresh token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=JWT_ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> dict:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except (jwt.InvalidTokenError, jwt.DecodeError, jwt.InvalidSignatureError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

# Global security manager instance
security_manager = SecurityManager()

# JWT Bearer scheme
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user."""
    try:
        payload = security_manager.verify_token(credentials.credentials)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get the current active user."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def require_permission(permission: str):
    """Decorator to require specific permissions."""
    def permission_checker(current_user: User = Depends(get_current_active_user)):
        if not current_user.has_permission(permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return permission_checker

def rate_limit(max_requests: int = 100, window_seconds: int = 3600):
    """Decorator to implement rate limiting."""
    def rate_limit_checker(request: Request):
        client_ip = request.client.host
        if not security_manager.check_rate_limit(client_ip, max_requests, window_seconds):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )
    return rate_limit_checker

def log_security_event(event_type: str, user_id: Optional[int] = None, details: Dict[str, Any] = None):
    """Log security events for monitoring."""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "user_id": user_id,
        "details": details or {}
    }
    logger.warning(f"SECURITY_EVENT: {log_data}")

# Security middleware
class SecurityMiddleware:
    """Middleware to add security headers and perform security checks."""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Add security headers
            async def send_with_headers(message):
                if message["type"] == "http.response.start":
                    headers = dict(message.get("headers", []))
                    for header, value in SECURITY_HEADERS.items():
                        headers[header.lower().encode()] = value.encode()
                    message["headers"] = list(headers.items())
                await send(message)
            
            await self.app(scope, receive, send_with_headers)
        else:
            await self.app(scope, receive, send) 