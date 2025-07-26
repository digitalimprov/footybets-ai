#!/usr/bin/env python3
"""
Script to create an admin user via the deployed API
This script will create your admin account on the live site.
"""

import requests
import json

# The deployed backend URL
BACKEND_URL = "https://footybets-backend-818397187963.us-central1.run.app"

def create_admin_user():
    """Create an admin user via the API."""
    
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
    
    # Prepare the user data
    user_data = {
        "email": email,
        "username": username,
        "password": password,
        "is_admin": True,
        "roles": ["admin"],
        "is_verified": True,
        "is_active": True
    }
    
    try:
        # First, try to register normally
        response = requests.post(f"{BACKEND_URL}/api/auth/register", json=user_data)
        
        if response.status_code == 200:
            print("✅ Admin user created successfully!")
            print(f"📧 Email: {email}")
            print(f"👤 Username: {username}")
            print(f"🔑 Password: {password}")
            print(f"👑 Role: Admin")
            print("\n🚀 You can now login with these credentials!")
            print(f"🌐 Login URL: https://footybets-frontend-wlbnzevhqa-uc.a.run.app/login")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"Response: {response.text}")
            
            # If registration failed, try to create via admin endpoint
            print("\n🔄 Trying admin creation endpoint...")
            admin_response = requests.post(f"{BACKEND_URL}/api/admin/users", json=user_data)
            
            if admin_response.status_code == 200:
                print("✅ Admin user created via admin endpoint!")
                print(f"📧 Email: {email}")
                print(f"👤 Username: {username}")
                print(f"🔑 Password: {password}")
                print(f"👑 Role: Admin")
                print("\n🚀 You can now login with these credentials!")
            else:
                print(f"❌ Admin creation also failed: {admin_response.status_code}")
                print(f"Response: {admin_response.text}")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        print("Make sure the backend is running and accessible.")

if __name__ == "__main__":
    create_admin_user() 