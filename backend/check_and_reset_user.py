#!/usr/bin/env python3
"""
Script to check user details and reset password for admin user.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.core.security import security_manager

def check_and_reset_user(email, new_password):
    """Check user details and reset password."""
    
    print(f"=== Checking and resetting user: {email} ===")
    
    # Use production database URL
    production_db_url = "postgresql://footybets_user:footybets_password@34.69.151.218:5432/footybets?sslmode=require"
    print(f"Database URL: {production_db_url}")
    
    try:
        # Create engine and session
        engine = create_engine(production_db_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Find the user
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print(f"✗ User with email {email} not found")
            return False
        
        print(f"✓ Found user: {user.username} (ID: {user.id})")
        print(f"Current roles: {user.roles}")
        print(f"Current is_admin: {user.is_admin}")
        print(f"Current is_verified: {user.is_verified}")
        print(f"Current is_active: {user.is_active}")
        
        # Reset password
        user.set_password(new_password)
        
        # Ensure user is active and verified
        user.is_active = True
        user.is_verified = True
        
        # Commit changes
        db.commit()
        db.refresh(user)
        
        print(f"✓ Successfully reset password for {email}!")
        print(f"New password: {new_password}")
        print(f"User is active: {user.is_active}")
        print(f"User is verified: {user.is_verified}")
        print(f"User is admin: {user.is_admin}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"✗ Error resetting user: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    email = "gmcintosh1985@gmail.com"
    new_password = "AdminPass123!"
    success = check_and_reset_user(email, new_password)
    
    if success:
        print("\n🎉 User password reset successfully!")
        print(f"Email: {email}")
        print(f"Password: {new_password}")
        print("You can now log in with these credentials.")
    else:
        print("\n❌ Failed to reset user password.") 