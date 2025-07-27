#!/usr/bin/env python3
"""
Debug script to test user registration and identify the exact error.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.core.config import settings
from app.core.security import security_manager

def test_registration():
    """Test the registration process step by step."""
    
    print("=== Registration Debug Test ===")
    
    # Test with production database URL
    production_db_url = "postgresql://footybets_user:footybets_password@34.69.151.218:5432/footybets?sslmode=require"
    print(f"Database URL: {production_db_url}")
    
    # Test database connection
    try:
        engine = create_engine(production_db_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
            print("✓ Database connection successful")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return
    
    # Test password validation
    test_password = "TestPass123!"
    try:
        validation = security_manager.validate_password_strength(test_password)
        print(f"✓ Password validation: {validation}")
    except Exception as e:
        print(f"✗ Password validation failed: {e}")
        return
    
    # Test password hashing
    try:
        hashed_password = security_manager.hash_password(test_password)
        print(f"✓ Password hashing successful: {hashed_password[:20]}...")
    except Exception as e:
        print(f"✗ Password hashing failed: {e}")
        return
    
    # Test user creation
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check if user exists
        existing_user = db.query(User).filter(
            (User.email == "test4@example.com") | (User.username == "testuser4")
        ).first()
        
        if existing_user:
            print("✗ Test user already exists")
            db.close()
            return
        
        # Create user object
        user = User(
            email="test4@example.com",
            username="testuser4",
            is_admin=True,
            is_verified=True,
            is_active=True,
            roles=["admin"],
            permissions=["read_predictions", "write_predictions", "read_analytics", "write_analytics", "read_games", "write_games", "read_users", "write_users", "read_system", "write_system", "manage_scraping", "manage_ai", "view_security_logs", "manage_roles", "export_data", "manage_subscriptions"]
        )
        print("✓ User object created")
        
        # Set password
        try:
            user.set_password(test_password)
            print("✓ Password set successfully")
        except Exception as e:
            print(f"✗ Password setting failed: {e}")
            import traceback
            traceback.print_exc()
            db.close()
            return
        
        # Add to database
        try:
            db.add(user)
            print("✓ User added to session")
        except Exception as e:
            print(f"✗ Adding user to session failed: {e}")
            import traceback
            traceback.print_exc()
            db.close()
            return
        
        # Commit
        try:
            db.commit()
            print("✓ User committed to database")
        except Exception as e:
            print(f"✗ Database commit failed: {e}")
            import traceback
            traceback.print_exc()
            db.rollback()
            db.close()
            return
        
        # Refresh
        try:
            db.refresh(user)
            print(f"✓ User refreshed, ID: {user.id}")
        except Exception as e:
            print(f"✗ User refresh failed: {e}")
            import traceback
            traceback.print_exc()
            db.close()
            return
        
        print("=== Registration successful! ===")
        db.close()
        
    except Exception as e:
        print(f"✗ User creation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_registration() 