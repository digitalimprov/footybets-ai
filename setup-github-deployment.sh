#!/bin/bash

# FootyBets.ai GitHub + Cloud Build Integration Setup
# This script sets up automatic deployments from GitHub to Google Cloud

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

echo -e "${BLUE}🚀 Setting up GitHub + Cloud Build Integration${NC}"
echo "=================================================="

# Check if gcloud is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${RED}❌ Not authenticated with Google Cloud. Please run:${NC}"
    echo "gcloud auth login"
    exit 1
fi

# Set project
echo -e "${BLUE}📋 Setting up project...${NC}"
gcloud config set project $PROJECT_ID

# Enable Cloud Build API
echo -e "${BLUE}🔧 Enabling Cloud Build API...${NC}"
gcloud services enable cloudbuild.googleapis.com

# Create Cloud Storage bucket for static files
echo -e "${BLUE}📁 Creating Cloud Storage bucket...${NC}"
gsutil mb -l $REGION gs://$PROJECT_ID-static || echo "Bucket already exists"
gsutil iam ch allUsers:objectViewer gs://$PROJECT_ID-static

# Upload Brownlow content
echo -e "${BLUE}📄 Uploading Brownlow content...${NC}"
cd backend/brownlow_web_content
gsutil -m cp -r . gs://$PROJECT_ID-static/brownlow-medal-predictions/
cd ../..

# Set up Cloud Build trigger
echo -e "${BLUE}🔗 Setting up Cloud Build trigger...${NC}"
echo -e "${YELLOW}Please provide your GitHub repository URL (e.g., https://github.com/username/footybets-ai):${NC}"
read -p "GitHub repo URL: " GITHUB_REPO_URL

# Extract repo name from URL
REPO_NAME=$(echo $GITHUB_REPO_URL | sed 's/.*github\.com\///' | sed 's/\.git$//')

# Create Cloud Build trigger
gcloud builds triggers create github \
    --repo-name=$REPO_NAME \
    --repo-owner=$(echo $REPO_NAME | cut -d'/' -f1) \
    --branch-pattern="^main$" \
    --build-config="cloudbuild.yaml" \
    --name="footybets-deploy-trigger" \
    --description="Deploy FootyBets.ai on push to main branch"

# Set up environment variables for Cloud Build
echo -e "${BLUE}🔐 Setting up environment variables...${NC}"
echo -e "${YELLOW}Please provide your Gemini API key:${NC}"
read -s -p "Gemini API Key: " GEMINI_API_KEY
echo

# Create a secret for the API key
echo $GEMINI_API_KEY | gcloud secrets create gemini-api-key --data-file=- || echo "Secret already exists"

# Grant Cloud Build access to the secret
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
gcloud secrets add-iam-policy-binding gemini-api-key \
    --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

# Update cloudbuild.yaml to use the secret
sed -i '' 's/your-gemini-api-key-here/\${_GEMINI_API_KEY}/' cloudbuild.yaml

echo -e "${GREEN}✅ GitHub integration setup complete!${NC}"
echo "=================================================="
echo -e "${BLUE}📋 Next steps:${NC}"
echo "1. Push your code to GitHub:"
echo "   git add ."
echo "   git commit -m 'Add Cloud Build configuration'"
echo "   git push origin main"
echo ""
echo "2. Your site will automatically deploy when you push to main branch"
echo ""
echo -e "${BLUE}🔗 Your deployment URLs:${NC}"
echo -e "  Frontend: ${GREEN}https://footybets-frontend-818397187963.us-central1.run.app${NC}"
echo -e "  Backend: ${GREEN}https://footybets-backend-818397187963.us-central1.run.app${NC}"
echo ""
echo -e "${GREEN}🚀 Your FootyBets.ai is now set up for automatic deployments!${NC}" 