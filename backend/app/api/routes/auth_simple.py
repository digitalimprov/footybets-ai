from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr
import re

from app.core.database import get_db
from app.models.user import User

router = APIRouter()

# Simplified Pydantic models
class UserRegisterSimple(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLoginSimple(BaseModel):
    email: EmailStr
    password: str

class TokenResponseSimple(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

@router.post("/register-simple", response_model=dict)
async def register_simple(
    user_data: UserRegisterSimple,
    db: Session = Depends(get_db)
):
    """Simple user registration without complex security features."""
    
    try:
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
        
        # Create new user with admin privileges for testing
        user = User(
            email=user_data.email,
            username=user_data.username,
            is_admin=True,  # Make admin for testing
            is_verified=True,  # Skip email verification
            is_active=True,
            roles=["admin"],
            permissions=["read_predictions", "write_predictions", "read_analytics", "write_analytics", "read_games", "write_games", "read_users", "write_users", "read_system", "write_system", "manage_scraping", "manage_ai", "view_security_logs", "manage_roles", "export_data", "manage_subscriptions"]
        )
        user.set_password(user_data.password)
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return {
            "message": "User registered successfully as admin!",
            "user_id": user.id,
            "email": user.email,
            "username": user.username,
            "is_admin": user.is_admin
        }
        
    except Exception as e:
        db.rollback()
        print(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login-simple", response_model=dict)
async def login_simple(
    form_data: UserLoginSimple,
    db: Session = Depends(get_db)
):
    """Simple user login."""
    
    try:
        # Find user by email
        user = db.query(User).filter(User.email == form_data.email).first()
        
        if not user or not user.verify_password(form_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is disabled"
            )
        
        # Create a simple token (in production, use proper JWT)
        token = f"simple_token_{user.id}_{datetime.utcnow().timestamp()}"
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "is_admin": user.is_admin,
                "roles": user.roles
            }
        }
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        ) 