#!/usr/bin/env python3
"""
Script to create an admin user for FootyBets.ai
Usage: python create_admin_user.py
"""

import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# Add the backend directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.user import User
from app.core.config import settings

# Initialize password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def create_admin_user():
    """Create an admin user for testing."""
    
    # Create database connection
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.email == "admin@footybets.ai").first()
        
        if admin_user:
            print("Admin user already exists!")
            if not admin_user.is_admin:
                admin_user.promote_to_admin()
                db.commit()
                print("Promoted existing user to admin.")
            return
        
        # Create new admin user
        admin_user = User(
            email="admin@footybets.ai",
            username="admin",
            hashed_password=hash_password("admin123"),
            full_name="System Administrator",
            is_active=True,
            is_verified=True
        )
        
        # Add to database
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        # Promote to admin
        admin_user.promote_to_admin()
        db.commit()
        
        print("✅ Admin user created successfully!")
        print("📧 Email: admin@footybets.ai")
        print("🔐 Password: admin123")
        print("⚠️  Please change the password after first login!")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user() 