from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr, validator
import re

from app.core.database import get_db
from app.core.security import security_manager, get_current_user, rate_limit, log_security_event
from app.models.user import User, UserSession, SecurityLog
from app.services.email_service import EmailService

router = APIRouter()

# Pydantic models for request/response
class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        validation = security_manager.validate_password_strength(v)
        if not validation["valid"]:
            raise ValueError(f"Password validation failed: {', '.join(validation['errors'])}")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False

class PasswordReset(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
    
    @validator('new_password')
    def validate_password(cls, v):
        validation = security_manager.validate_password_strength(v)
        if not validation["valid"]:
            raise ValueError(f"Password validation failed: {', '.join(validation['errors'])}")
        return v

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    is_active: bool
    is_verified: bool
    is_admin: bool
    roles: list
    permissions: list
    created_at: Optional[str]
    last_login: Optional[str]

    class Config:
        from_attributes = True

@router.post("/register", response_model=dict)
async def register(
    user_data: UserRegister,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Register a new user with security validation."""
    
    # Rate limiting
    client_ip = request.client.host
    if not security_manager.check_rate_limit(f"register_{client_ip}", max_requests=5, window_seconds=3600):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many registration attempts. Please try again later."
        )
    
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        if existing_user.email == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Create new user
    user = User(
        email=user_data.email,
        username=user_data.username
    )
    
    # Set password with proper error handling
    try:
        user.set_password(user_data.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    # Generate verification token
    verification_token = user.generate_verification_token()
    
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Log security event
        log_security_event("user_registered", user.id, {
            "ip_address": client_ip,
            "user_agent": request.headers.get("user-agent")
        })
        
        # Send verification email in background
        background_tasks.add_task(
            EmailService.send_verification_email,
            user.email,
            verification_token
        )
        
        return {
            "message": "User registered successfully. Please check your email to verify your account.",
            "user_id": user.id
        }
        
    except Exception as e:
        db.rollback()
        log_security_event("registration_failed", None, {
            "email": user_data.email,
            "error": str(e),
            "ip_address": client_ip
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again."
        )

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    """Authenticate user and return JWT tokens."""
    
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "")
    
    # Check for account lockout
    if security_manager.is_account_locked(form_data.email):
        log_security_event("login_attempt_locked_account", None, {
            "email": form_data.email,
            "ip_address": client_ip
        })
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="Account is temporarily locked due to too many failed login attempts."
        )
    
    # Rate limiting for login attempts
    if not security_manager.check_rate_limit(f"login_{client_ip}", max_requests=10, window_seconds=300):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later."
        )
    
    # Find user
    user = db.query(User).filter(User.email == form_data.email).first()
    if not user:
        security_manager.track_failed_login(form_data.email)
        log_security_event("login_failed_invalid_email", None, {
            "email": form_data.email,
            "ip_address": client_ip
        })
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if account is locked
    if user.is_locked:
        log_security_event("login_attempt_locked_user", user.id, {
            "ip_address": client_ip
        })
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="Account is locked. Please contact support."
        )
    
    # Verify password
    if not user.verify_password(form_data.password):
        user.record_failed_login()
        db.commit()
        
        log_security_event("login_failed_invalid_password", user.id, {
            "ip_address": client_ip
        })
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if account is active
    if not user.is_active:
        log_security_event("login_attempt_inactive_account", user.id, {
            "ip_address": client_ip
        })
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated"
        )
    
    # Successful login
    user.record_successful_login()
    
    # Create session
    session = UserSession(
        user_id=user.id,
        session_token=security_manager.generate_secure_token(),
        ip_address=client_ip,
        user_agent=user_agent
    )
    
    # Set token expiration
    if form_data.remember_me:
        access_token_expires = timedelta(days=7)
        session.expires_at = datetime.utcnow() + timedelta(days=30)
    else:
        access_token_expires = timedelta(minutes=30)
        session.expires_at = datetime.utcnow() + timedelta(days=1)
    
    # Create tokens
    access_token = security_manager.create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=access_token_expires
    )
    refresh_token = security_manager.create_refresh_token(
        data={"sub": user.id, "email": user.email}
    )
    
    try:
        db.add(session)
        db.commit()
        
        # Log successful login
        log_security_event("login_successful", user.id, {
            "ip_address": client_ip,
            "session_id": session.id
        })
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=access_token_expires.total_seconds(),
            user=user.to_dict()
        )
        
    except Exception as e:
        db.rollback()
        log_security_event("login_session_creation_failed", user.id, {
            "error": str(e),
            "ip_address": client_ip
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed. Please try again."
        )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token."""
    
    try:
        payload = security_manager.verify_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Create new access token
        access_token = security_manager.create_access_token(
            data={"sub": user.id, "email": user.email}
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=1800,  # 30 minutes
            user=user.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        log_security_event("token_refresh_failed", None, {
            "error": str(e),
            "ip_address": request.client.host
        })
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.post("/logout")
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout user and invalidate session."""
    
    # Get session token from request
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        
        # Find and deactivate session
        session = db.query(UserSession).filter(
            UserSession.user_id == current_user.id,
            UserSession.is_active == True
        ).first()
        
        if session:
            session.deactivate()
            db.commit()
    
    log_security_event("logout", current_user.id, {
        "ip_address": request.client.host
    })
    
    return {"message": "Successfully logged out"}

@router.post("/password-reset")
async def request_password_reset(
    password_reset: PasswordReset,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Request password reset via email."""
    
    # Rate limiting
    client_ip = request.client.host
    if not security_manager.check_rate_limit(f"password_reset_{client_ip}", max_requests=3, window_seconds=3600):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many password reset requests. Please try again later."
        )
    
    user = db.query(User).filter(User.email == password_reset.email).first()
    if user:
        reset_token = user.generate_password_reset_token()
        db.commit()
        
        # Send password reset email in background
        background_tasks.add_task(
            EmailService.send_password_reset_email,
            user.email,
            reset_token
        )
        
        log_security_event("password_reset_requested", user.id, {
            "ip_address": client_ip
        })
    
    # Always return success to prevent email enumeration
    return {"message": "If the email exists, a password reset link has been sent."}

@router.post("/password-reset/confirm")
async def confirm_password_reset(
    password_reset: PasswordResetConfirm,
    request: Request,
    db: Session = Depends(get_db)
):
    """Confirm password reset with token."""
    
    user = db.query(User).filter(User.password_reset_token == password_reset.token).first()
    
    if not user or not user.verify_password_reset_token(password_reset.token):
        log_security_event("password_reset_invalid_token", None, {
            "token": password_reset.token,
            "ip_address": request.client.host
        })
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Set new password
    user.set_password(password_reset.new_password)
    user.clear_password_reset_token()
    db.commit()
    
    log_security_event("password_reset_successful", user.id, {
        "ip_address": request.client.host
    })
    
    return {"message": "Password reset successfully"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user

@router.post("/verify-email/{token}")
async def verify_email(
    token: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Verify user email with token."""
    
    user = db.query(User).filter(User.email_verification_token == token).first()
    
    if not user:
        log_security_event("email_verification_invalid_token", None, {
            "token": token,
            "ip_address": request.client.host
        })
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token"
        )
    
    user.is_verified = True
    user.email_verification_token = None
    db.commit()
    
    log_security_event("email_verification_successful", user.id, {
        "ip_address": request.client.host
    })
    
    return {"message": "Email verified successfully"}

@router.post("/resend-verification")
async def resend_verification_email(
    email: EmailStr,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Resend email verification."""
    
    # Rate limiting
    client_ip = request.client.host
    if not security_manager.check_rate_limit(f"resend_verification_{client_ip}", max_requests=3, window_seconds=3600):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many verification email requests. Please try again later."
        )
    
    user = db.query(User).filter(User.email == email).first()
    if user and not user.is_verified:
        verification_token = user.generate_verification_token()
        db.commit()
        
        background_tasks.add_task(
            EmailService.send_verification_email,
            user.email,
            verification_token
        )
        
        log_security_event("verification_email_resent", user.id, {
            "ip_address": client_ip
        })
    
    return {"message": "If the email exists and is not verified, a verification email has been sent."} 