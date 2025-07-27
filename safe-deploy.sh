#!/bin/bash

# Safe Deployment Script for FootyBets AI - Hybrid Approach
# This script ensures safe deployment with enhanced AI predictions

set -e  # Exit on any error

echo "🚀 Starting safe deployment for FootyBets AI..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Pre-deployment checks
print_status "Performing pre-deployment checks..."

# Check if we're in the right directory
if [ ! -f "cloudbuild.yaml" ]; then
    print_error "cloudbuild.yaml not found. Please run this script from the project root."
    exit 1
fi

# Check for large files that shouldn't be deployed
print_status "Checking for large files..."
LARGE_FILES=$(find . -name "*.json" -size +10M 2>/dev/null | head -5)
if [ ! -z "$LARGE_FILES" ]; then
    print_warning "Large JSON files found (these will be included in deployment):"
    echo "$LARGE_FILES"
    echo ""
    read -p "Continue with deployment? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Deployment cancelled."
        exit 0
    fi
fi

# Check database files (should not be deployed)
DB_FILES=$(find . -name "*.db" -o -name "*.sqlite" -o -name "*.sqlite3" 2>/dev/null)
if [ ! -z "$DB_FILES" ]; then
    print_warning "Database files found (these should be ignored by .gitignore):"
    echo "$DB_FILES"
fi

# Build frontend with correct API URL
print_status "Building frontend with correct API URL..."
cd frontend

# Clean previous build
if [ -d "build" ]; then
    print_status "Cleaning previous build..."
    rm -rf build
fi

# Build with correct environment variable
print_status "Building frontend..."
REACT_APP_API_URL=https://footybets-backend-wlbnzevhqa-uc.a.run.app npm run build

# Verify the build contains correct API URL
print_status "Verifying build contains correct API URL..."
if grep -q "footybets-backend-wlbnzevhqa-uc.a.run.app" build/static/js/*.js; then
    print_success "Frontend build contains correct API URL"
else
    print_warning "Could not verify API URL in build (this might be normal)"
fi

# Check for localhost URLs in build
if grep -q "localhost:8000" build/static/js/*.js; then
    print_error "Build still contains localhost URLs!"
    exit 1
fi

cd ..

# Verify backend files
print_status "Checking backend configuration..."
if [ ! -f "backend/app/ai/predictor.py" ]; then
    print_error "Enhanced predictor not found!"
    exit 1
fi

# Check if JSON data files exist
print_status "Checking JSON data files..."
JSON_FILES=(
    "backend/brownlow_analysis_2024.json"
    "backend/afl_2025_games_20250725_201541.json"
    "backend/afl_2025_games_with_stats_20250725_202121.json"
)

for file in "${JSON_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_success "Found: $file"
    else
        print_warning "Missing: $file (AI will work with reduced context)"
    fi
done

# Deploy using Cloud Build
print_status "Starting Cloud Build deployment..."
gcloud builds submit --config cloudbuild.yaml .

if [ $? -eq 0 ]; then
    print_success "Deployment completed successfully!"
    
    # Wait for deployment to propagate
    print_status "Waiting for deployment to propagate..."
    sleep 30
    
    # Test the predictions endpoint
    print_status "Testing predictions endpoint..."
    RESPONSE=$(curl -s -w "%{http_code}" "https://footybets-backend-wlbnzevhqa-uc.a.run.app/api/predictions/?limit=5" -H "Origin: https://footybets.ai")
    HTTP_CODE="${RESPONSE: -3}"
    RESPONSE_BODY="${RESPONSE%???}"
    
    if [ "$HTTP_CODE" = "200" ]; then
        print_success "Predictions endpoint is working correctly"
        echo "Response: $RESPONSE_BODY"
    else
        print_warning "Predictions endpoint returned HTTP $HTTP_CODE"
        echo "Response: $RESPONSE_BODY"
    fi
    
    print_success "🎉 Deployment completed successfully!"
    print_status "Your enhanced AI predictions are now live at https://footybets.ai"
    
else
    print_error "Deployment failed!"
    exit 1
fi 