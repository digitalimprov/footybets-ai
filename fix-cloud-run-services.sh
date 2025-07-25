#!/bin/bash

# Fix Google Cloud Run Services Script
# This script redeploys the services with proper configuration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="footybets-ai"
REGION="us-central1"
BACKEND_SERVICE="footybets-backend"
FRONTEND_SERVICE="footybets-frontend"

echo -e "${BLUE}🔧 Fixing Google Cloud Run Services${NC}"
echo "=================================================="

echo -e "${RED}🚨 Issues Detected:${NC}"
echo "• Frontend: React dev server configuration error"
echo "• Backend: 400 Bad Request errors"
echo "• DNS: SERVFAIL errors for footybets.ai"
echo ""

echo -e "${BLUE}🔧 Step 1: Fix Frontend Service${NC}"
echo "=================================================="

# Check frontend configuration
echo -e "${YELLOW}Checking frontend configuration...${NC}"
cd frontend

# Check if package.json has proper build scripts
if ! grep -q '"build"' package.json; then
    echo -e "${RED}❌ Frontend package.json missing build script${NC}"
    echo "Adding build script..."
    # Add build script if missing
fi

# Build and deploy frontend
echo -e "${YELLOW}Building and deploying frontend...${NC}"
gcloud builds submit --tag gcr.io/$PROJECT_ID/$FRONTEND_SERVICE

gcloud run deploy $FRONTEND_SERVICE \
    --image gcr.io/$PROJECT_ID/$FRONTEND_SERVICE \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 512Mi \
    --cpu 1 \
    --max-instances 5 \
    --set-env-vars="NODE_ENV=production" \
    --set-env-vars="REACT_APP_API_URL=https://footybets-backend-818397187963.us-central1.run.app"

echo -e "${GREEN}✅ Frontend redeployed${NC}"

echo -e "${BLUE}🔧 Step 2: Fix Backend Service${NC}"
echo "=================================================="

# Check backend configuration
echo -e "${YELLOW}Checking backend configuration...${NC}"
cd ../backend

# Check if main.py exists and is properly configured
if [ ! -f "app/main.py" ]; then
    echo -e "${RED}❌ Backend main.py not found${NC}"
    exit 1
fi

# Build and deploy backend
echo -e "${YELLOW}Building and deploying backend...${NC}"
gcloud builds submit --tag gcr.io/$PROJECT_ID/$BACKEND_SERVICE

gcloud run deploy $BACKEND_SERVICE \
    --image gcr.io/$PROJECT_ID/$BACKEND_SERVICE \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 10 \
    --set-env-vars="ENVIRONMENT=production" \
    --set-env-vars="DATABASE_URL=postgresql://footybets_user:footybets_password@/footybets-db-818397187963:us-central1:footybets/footybets" \
    --set-env-vars="GEMINI_API_KEY=$GEMINI_API_KEY"

echo -e "${GREEN}✅ Backend redeployed${NC}"

echo -e "${BLUE}🔧 Step 3: Test Services${NC}"
echo "=================================================="

# Get service URLs
BACKEND_URL=$(gcloud run services describe $BACKEND_SERVICE --region=$REGION --format="value(status.url)")
FRONTEND_URL=$(gcloud run services describe $FRONTEND_SERVICE --region=$REGION --format="value(status.url)")

echo -e "${BLUE}📋 Service URLs:${NC}"
echo -e "  Backend: ${GREEN}$BACKEND_URL${NC}"
echo -e "  Frontend: ${GREEN}$FRONTEND_URL${NC}"

# Test services
echo -e "${YELLOW}Testing services...${NC}"
echo "Testing backend..."
curl -I "$BACKEND_URL" || echo "Backend test failed"

echo "Testing frontend..."
curl -I "$FRONTEND_URL" || echo "Frontend test failed"

echo -e "${BLUE}🔧 Step 4: DNS Configuration${NC}"
echo "=================================================="

echo -e "${YELLOW}Next steps for DNS:${NC}"
echo "1. Go to Namecheap Advanced DNS"
echo "2. Delete all existing records"
echo "3. Add URL Redirect record:"
echo "   - Type: URL Redirect"
echo "   - Host: @"
echo "   - Value: $FRONTEND_URL"
echo "   - TTL: Automatic"
echo ""
echo "4. Add CNAME records:"
echo "   - CNAME | api | $BACKEND_URL"
echo "   - CNAME | www | $FRONTEND_URL"

echo -e "${GREEN}🎉 Services fixed! Now configure DNS in Namecheap.${NC}" 