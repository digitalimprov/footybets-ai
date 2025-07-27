#!/usr/bin/env python3
"""
Simple signup test to debug the 500 error
"""

import requests
import json
import time

def test_signup():
    """Test signup with minimal data"""
    
    backend_url = "https://footybets-backend-wlbnzevhqa-uc.a.run.app"
    
    # Test data
    test_data = {
        "email": f"test{int(time.time())}@example.com",
        "username": f"testuser{int(time.time())}",
        "password": "TestPassword123!"
    }
    
    print(f"Testing signup with data: {test_data}")
    
    try:
        # Test the signup endpoint
        response = requests.post(
            f"{backend_url}/api/auth/register",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print("✅ Signup successful!")
        else:
            print("❌ Signup failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_signup() 