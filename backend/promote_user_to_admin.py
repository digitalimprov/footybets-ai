#!/usr/bin/env python3
"""
Script to promote a user to admin role.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.core.config import settings

def promote_user_to_admin(email):
    """Promote a user to admin role."""
    
    print(f"=== Promoting {email} to admin ===")
    
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
        
        # Promote to admin
        user.is_admin = True
        if "admin" not in user.roles:
            user.roles.append("admin")
        user.subscription_tier = "admin"
        user.subscription_expires = None  # Admin subscription never expires
        
        # Update permissions
        user._update_permissions()
        
        # Commit changes
        db.commit()
        db.refresh(user)
        
        print(f"✓ Successfully promoted {email} to admin!")
        print(f"New roles: {user.roles}")
        print(f"New is_admin: {user.is_admin}")
        print(f"New permissions: {user.permissions}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"✗ Error promoting user: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    email = "gmcintosh1985@gmail.com"
    success = promote_user_to_admin(email)
    
    if success:
        print("\n🎉 User successfully promoted to admin!")
        print("You can now log in with admin privileges.")
    else:
        print("\n❌ Failed to promote user to admin.") 