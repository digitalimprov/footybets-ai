#!/bin/bash

# FootyBets.ai Quick Update Deployment Script
# Use this for immediate deployments without GitHub integration

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

echo -e "${BLUE}🚀 FootyBets.ai Quick Update Deployment${NC}"
echo "=================================================="

# Check if gcloud is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${RED}❌ Not authenticated with Google Cloud. Please run:${NC}"
    echo "gcloud auth login"
    exit 1
fi

# Set project
gcloud config set project $PROJECT_ID

# Deploy backend
echo -e "${BLUE}🔨 Deploying backend...${NC}"
cd backend
gcloud builds submit --tag gcr.io/$PROJECT_ID/footybets-backend

gcloud run deploy footybets-backend \
    --image gcr.io/$PROJECT_ID/footybets-backend \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 10 \
    --set-env-vars="DATABASE_URL=postgresql://footybets_user:footybets_password@/footybets-ai:us-central1:footybets-db/footybets" \
    --set-env-vars="GEMINI_API_KEY=$GEMINI_API_KEY" \
    --set-env-vars="ENVIRONMENT=production"

BACKEND_URL=$(gcloud run services describe footybets-backend --region=$REGION --format="value(status.url)")
echo -e "${GREEN}✅ Backend updated: $BACKEND_URL${NC}"

# Deploy frontend
echo -e "${BLUE}🔨 Deploying frontend...${NC}"
cd ../frontend
gcloud builds submit --tag gcr.io/$PROJECT_ID/footybets-frontend

gcloud run deploy footybets-frontend \
    --image gcr.io/$PROJECT_ID/footybets-frontend \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 512Mi \
    --cpu 1 \
    --max-instances 5 \
    --set-env-vars="REACT_APP_API_URL=$BACKEND_URL"

FRONTEND_URL=$(gcloud run services describe footybets-frontend --region=$REGION --format="value(status.url)")
echo -e "${GREEN}✅ Frontend updated: $FRONTEND_URL${NC}"

# Update Cloud Storage if Brownlow content changed
echo -e "${BLUE}📄 Updating Brownlow content...${NC}"
cd ../backend/brownlow_web_content
gsutil -m cp -r . gs://$PROJECT_ID-static/brownlow-medal-predictions/

echo -e "${GREEN}🎉 Update deployment completed!${NC}"
echo "=================================================="
echo -e "${BLUE}🔗 Your updated URLs:${NC}"
echo -e "  Frontend: ${GREEN}$FRONTEND_URL${NC}"
echo -e "  Backend: ${GREEN}$BACKEND_URL${NC}"
echo ""
echo -e "${GREEN}🚀 Your FootyBets.ai has been updated!${NC}" 