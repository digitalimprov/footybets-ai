#!/usr/bin/env python3
"""
Script to create an admin user for FootyBets.ai
Run this script to create your admin account.
"""

import sys
import os
from datetime import datetime, timedelta

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.user import User, ROLE_PERMISSIONS
from app.core.security import security_manager

def create_admin_user(email: str, username: str, password: str):
    """Create an admin user with full permissions."""
    
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()
        
        if existing_user:
            print(f"❌ User with email '{email}' or username '{username}' already exists!")
            return False
        
        # Create admin user
        admin_user = User(
            email=email,
            username=username,
            is_active=True,
            is_verified=True,
            is_admin=True,
            roles=["admin"],
            permissions=ROLE_PERMISSIONS["admin"],
            subscription_tier="admin",
            subscription_expires=datetime.utcnow() + timedelta(days=365*10)  # 10 years
        )
        
        # Set password
        admin_user.set_password(password)
        
        # Add to database
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Admin user created successfully!")
        print(f"📧 Email: {email}")
        print(f"👤 Username: {username}")
        print(f"🔑 Password: {password}")
        print(f"👑 Role: Admin")
        print(f"🔐 Permissions: {len(admin_user.permissions)} permissions")
        print(f"📅 Subscription: Admin (expires in 10 years)")
        print("\n🚀 You can now login with these credentials!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def main():
    print("🔧 FootyBets.ai Admin User Creator")
    print("=" * 40)
    
    # Get admin details
    email = input("Enter admin email: ").strip()
    username = input("Enter admin username: ").strip()
    password = input("Enter admin password: ").strip()
    
    if not email or not username or not password:
        print("❌ Email, username, and password are required!")
        return
    
    if len(password) < 8:
        print("❌ Password must be at least 8 characters long!")
        return
    
    print(f"\n📝 Creating admin user...")
    print(f"Email: {email}")
    print(f"Username: {username}")
    
    confirm = input("\nProceed? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled.")
        return
    
    success = create_admin_user(email, username, password)
    
    if success:
        print("\n🎉 Admin user created successfully!")
        print("You can now login to the admin panel.")
    else:
        print("\n❌ Failed to create admin user.")

if __name__ == "__main__":
    main() 