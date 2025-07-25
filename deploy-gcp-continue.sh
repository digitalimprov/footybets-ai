#!/bin/bash

# FootyBets.ai Google Cloud Deployment Continuation Script
# This script continues deployment after database is created

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
ZONE="us-central1-a"

# Services
BACKEND_SERVICE="footybets-backend"
FRONTEND_SERVICE="footybets-frontend"
DATABASE_INSTANCE="footybets-db"

echo -e "${BLUE}🚀 FootyBets.ai Google Cloud Deployment (Continuation)${NC}"
echo "=================================================="

# Check if database is ready
echo -e "${BLUE}🗄️  Checking database status...${NC}"
DB_STATUS=$(gcloud sql instances describe $DATABASE_INSTANCE --format="value(state)")

if [ "$DB_STATUS" != "RUNNABLE" ]; then
    echo -e "${YELLOW}⏳ Database is still being created. Status: $DB_STATUS${NC}"
    echo -e "${YELLOW}Please wait for database to be ready and run this script again.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Database is ready!${NC}"

# Create database if it doesn't exist
echo -e "${BLUE}📊 Creating database...${NC}"
gcloud sql databases create footybets --instance=$DATABASE_INSTANCE || echo "Database already exists"

# Create database user if it doesn't exist
echo -e "${BLUE}👤 Creating database user...${NC}"
gcloud sql users create footybets_user --instance=$DATABASE_INSTANCE --password=footybets_password || echo "User already exists"

# Get database connection info
DB_HOST=$(gcloud sql instances describe $DATABASE_INSTANCE --format="value(connectionName)")
echo -e "${GREEN}✅ Database ready: $DB_HOST${NC}"

# Build and deploy backend
echo -e "${BLUE}🔨 Building and deploying backend...${NC}"
cd backend
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
    --set-env-vars="DATABASE_URL=postgresql://footybets_user:footybets_password@/$DB_HOST/footybets" \
    --set-env-vars="GEMINI_API_KEY=$GEMINI_API_KEY" \
    --set-env-vars="ENVIRONMENT=production"

BACKEND_URL=$(gcloud run services describe $BACKEND_SERVICE --region=$REGION --format="value(status.url)")
echo -e "${GREEN}✅ Backend deployed: $BACKEND_URL${NC}"

# Build and deploy frontend
echo -e "${BLUE}🔨 Building and deploying frontend...${NC}"
cd ../frontend
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
    --set-env-vars="REACT_APP_API_URL=$BACKEND_URL"

FRONTEND_URL=$(gcloud run services describe $FRONTEND_SERVICE --region=$REGION --format="value(status.url)")
echo -e "${GREEN}✅ Frontend deployed: $FRONTEND_URL${NC}"

# Setup Cloud Storage for static files
echo -e "${BLUE}📁 Setting up Cloud Storage...${NC}"
gsutil mb -l $REGION gs://$PROJECT_ID-static || echo "Bucket already exists"
gsutil iam ch allUsers:objectViewer gs://$PROJECT_ID-static

# Copy Brownlow content to Cloud Storage
echo -e "${BLUE}📄 Uploading Brownlow content...${NC}"
cd ../backend/brownlow_web_content
gsutil -m cp -r . gs://$PROJECT_ID-static/brownlow-medal-predictions/

echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo "=================================================="
echo -e "${BLUE}📊 Services:${NC}"
echo -e "  Backend: ${GREEN}$BACKEND_URL${NC}"
echo -e "  Frontend: ${GREEN}$FRONTEND_URL${NC}"
echo -e "  Database: ${GREEN}$DB_HOST${NC}"
echo -e "  Storage: ${GREEN}gs://$PROJECT_ID-static${NC}"
echo ""
echo -e "${BLUE}🔧 Next steps:${NC}"
echo "1. Set up custom domain mapping"
echo "2. Configure SSL certificates"
echo "3. Set up monitoring and logging"
echo "4. Configure backup schedules"
echo ""
echo -e "${GREEN}🚀 Your FootyBets.ai platform is now live on Google Cloud!${NC}" 