#!/bin/bash

# FootyBets.ai Google Cloud Deployment Script
# This script deploys the complete application to Google Cloud Platform

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

echo -e "${BLUE}🚀 FootyBets.ai Google Cloud Deployment${NC}"
echo "=================================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Google Cloud CLI not found. Please install it first:${NC}"
    echo "Visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${YELLOW}⚠️  Not authenticated with Google Cloud. Please run:${NC}"
    echo "gcloud auth login"
    exit 1
fi

# Set project
echo -e "${BLUE}📋 Setting up project...${NC}"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo -e "${BLUE}🔧 Enabling required APIs...${NC}"
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    sqladmin.googleapis.com \
    storage.googleapis.com \
    compute.googleapis.com

# Create Cloud SQL instance
echo -e "${BLUE}🗄️  Creating Cloud SQL instance...${NC}"
gcloud sql instances create $DATABASE_INSTANCE \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=$REGION \
    --storage-type=SSD \
    --storage-size=10GB \
    --backup-start-time=02:00 \
    --maintenance-window-day=SUN \
    --maintenance-window-hour=2 \
    --availability-type=zonal \
    --storage-auto-increase

# Create database
echo -e "${BLUE}📊 Creating database...${NC}"
gcloud sql databases create footybets --instance=$DATABASE_INSTANCE

# Create database user
echo -e "${BLUE}👤 Creating database user...${NC}"
gcloud sql users create footybets_user \
    --instance=$DATABASE_INSTANCE \
    --password=footybets_password

# Get database connection info
DB_HOST=$(gcloud sql instances describe $DATABASE_INSTANCE --format="value(connectionName)")
echo -e "${GREEN}✅ Database created: $DB_HOST${NC}"

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

# Create custom domain mapping (optional)
echo -e "${BLUE}🌐 Setting up custom domain...${NC}"
echo -e "${YELLOW}To set up custom domain, run:${NC}"
echo "gcloud run domain-mappings create --service=$FRONTEND_SERVICE --domain=footybets.ai --region=$REGION"

# Setup Cloud Storage for static files
echo -e "${BLUE}📁 Setting up Cloud Storage...${NC}"
gsutil mb -l $REGION gs://$PROJECT_ID-static
gsutil iam ch allUsers:objectViewer gs://$PROJECT_ID-static

# Copy Brownlow content to Cloud Storage
echo -e "${BLUE}📄 Uploading Brownlow content...${NC}"
cd ../backend/brownlow_web_content
gsutil -m cp -r . gs://$PROJECT_ID-static/brownlow-medal-predictions/

# Create load balancer (optional)
echo -e "${BLUE}⚖️  Setting up load balancer...${NC}"
echo -e "${YELLOW}To create a load balancer, run:${NC}"
echo "gcloud compute url-maps create footybets-lb --default-service=$FRONTEND_SERVICE"

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