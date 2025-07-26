#!/usr/bin/env python3
"""
Network debugging script for FootyBets.ai
Tests all aspects of connectivity to identify signup issues
"""

import requests
import json
import time
import sys
import os
from datetime import datetime

# Configuration
FRONTEND_URL = "https://footybets.ai"
BACKEND_URL = "https://footybets-backend-wlbnzevhqa-uc.a.run.app"
CLOUD_FRONTEND_URL = "https://footybets-frontend-wlbnzevhqa-uc.a.run.app"

def log(message, level="INFO"):
    """Log messages with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

def test_endpoint(url, endpoint="/", method="GET", data=None, headers=None):
    """Test a specific endpoint"""
    try:
        full_url = f"{url}{endpoint}"
        log(f"Testing {method} {full_url}")
        
        if method == "GET":
            response = requests.get(full_url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(full_url, json=data, headers=headers, timeout=10)
        
        log(f"Status: {response.status_code}")
        log(f"Headers: {dict(response.headers)}")
        
        if response.status_code < 400:
            try:
                log(f"Response: {response.json()}")
            except:
                log(f"Response: {response.text[:200]}...")
        else:
            log(f"Error Response: {response.text}")
            
        return response
        
    except requests.exceptions.RequestException as e:
        log(f"Request failed: {str(e)}", "ERROR")
        return None

def test_cors_preflight():
    """Test CORS preflight request"""
    log("Testing CORS preflight...")
    
    headers = {
        'Origin': FRONTEND_URL,
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type,Authorization'
    }
    
    response = requests.options(f"{BACKEND_URL}/api/auth/register", headers=headers, timeout=10)
    log(f"CORS preflight status: {response.status_code}")
    log(f"CORS headers: {dict(response.headers)}")
    return response

def test_signup_request():
    """Test actual signup request"""
    log("Testing signup request...")
    
    signup_data = {
        "email": f"test{int(time.time())}@example.com",
        "username": f"testuser{int(time.time())}",
        "password": "TestPassword123!"
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Origin': FRONTEND_URL
    }
    
    response = requests.post(f"{BACKEND_URL}/api/auth/register", 
                           json=signup_data, 
                           headers=headers, 
                           timeout=10)
    
    log(f"Signup response status: {response.status_code}")
    log(f"Signup response: {response.text}")
    return response

def test_frontend_config():
    """Test frontend configuration"""
    log("Testing frontend configuration...")
    
    # Test if frontend loads
    response = requests.get(FRONTEND_URL, timeout=10)
    log(f"Frontend status: {response.status_code}")
    
    # Look for API URL in the HTML
    if "REACT_APP_API_URL" in response.text or "localhost:8000" in response.text:
        log("Found API URL configuration in frontend", "WARNING")
    
    return response

def main():
    """Main debugging function"""
    log("🔍 Starting comprehensive network debugging...")
    log(f"Frontend URL: {FRONTEND_URL}")
    log(f"Backend URL: {BACKEND_URL}")
    
    # Test 1: Backend health
    log("\n=== Test 1: Backend Health ===")
    test_endpoint(BACKEND_URL, "/health")
    
    # Test 2: CORS preflight
    log("\n=== Test 2: CORS Preflight ===")
    test_cors_preflight()
    
    # Test 3: Frontend configuration
    log("\n=== Test 3: Frontend Configuration ===")
    test_frontend_config()
    
    # Test 4: Signup endpoint
    log("\n=== Test 4: Signup Endpoint ===")
    test_signup_request()
    
    # Test 5: Cloud Run URLs
    log("\n=== Test 5: Cloud Run URLs ===")
    test_endpoint(CLOUD_FRONTEND_URL, "/")
    test_endpoint(BACKEND_URL, "/health")
    
    log("\n🔍 Debugging complete!")

if __name__ == "__main__":
    main() 