# 🚀 Google Cloud Deployment Guide for FootyBets.ai

This guide will help you deploy FootyBets.ai to Google Cloud Platform using Cloud Run, Cloud SQL, and Cloud Storage.

## 📋 Prerequisites

### 1. Google Cloud Account
- Create a Google Cloud account at [cloud.google.com](https://cloud.google.com)
- Enable billing for your project
- Note: New accounts get $300 free credit

### 2. Install Google Cloud CLI

**macOS (using Homebrew):**
```bash
brew install --cask google-cloud-sdk
```

**macOS (manual install):**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

**Windows:**
Download from [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)

### 3. Authentication
```bash
gcloud auth login
gcloud auth application-default login
```

## 🎯 Quick Deployment

### Step 1: Create Google Cloud Project
```bash
# Create new project (or use existing)
gcloud projects create footybets-ai --name="FootyBets AI"

# Set as default project
gcloud config set project footybets-ai
```

### Step 2: Set Environment Variables
```bash
# Set your Gemini API key
export GEMINI_API_KEY="your_gemini_api_key_here"

# Set your project ID
export PROJECT_ID="footybets-ai"
```

### Step 3: Run Deployment Script
```bash
# Make script executable (if not already)
chmod +x deploy-gcp.sh

# Run deployment
./deploy-gcp.sh
```

## 🔧 Manual Deployment Steps

If you prefer to deploy manually, follow these steps:

### 1. Enable Required APIs
```bash
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    sqladmin.googleapis.com \
    storage.googleapis.com \
    compute.googleapis.com
```

### 2. Create Cloud SQL Database
```bash
# Create PostgreSQL instance
gcloud sql instances create footybets-db \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=us-central1 \
    --storage-type=SSD \
    --storage-size=10GB \
    --backup-start-time=02:00 \
    --maintenance-window-day=SUN \
    --maintenance-window-hour=02:00

# Create database
gcloud sql databases create footybets --instance=footybets-db

# Create user
gcloud sql users create footybets_user \
    --instance=footybets-db \
    --password=footybets_password
```

### 3. Deploy Backend
```bash
cd backend

# Build and push image
gcloud builds submit --tag gcr.io/footybets-ai/footybets-backend

# Deploy to Cloud Run
gcloud run deploy footybets-backend \
    --image gcr.io/footybets-ai/footybets-backend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 10 \
    --set-env-vars="DATABASE_URL=postgresql://footybets_user:footybets_password@/footybets-ai:us-central1:footybets-db/footybets" \
    --set-env-vars="GEMINI_API_KEY=$GEMINI_API_KEY" \
    --set-env-vars="ENVIRONMENT=production"
```

### 4. Deploy Frontend
```bash
cd ../frontend

# Build and push image
gcloud builds submit --tag gcr.io/footybets-ai/footybets-frontend

# Deploy to Cloud Run
gcloud run deploy footybets-frontend \
    --image gcr.io/footybets-ai/footybets-frontend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8080 \
    --memory 512Mi \
    --cpu 1 \
    --max-instances 5 \
    --set-env-vars="REACT_APP_API_URL=$BACKEND_URL"
```

### 5. Setup Cloud Storage
```bash
# Create bucket for static files
gsutil mb -l us-central1 gs://footybets-ai-static

# Make bucket public
gsutil iam ch allUsers:objectViewer gs://footybets-ai-static

# Upload Brownlow content
cd ../backend/brownlow_web_content
gsutil -m cp -r . gs://footybets-ai-static/brownlow-medal-predictions/
```

## 🌐 Custom Domain Setup

### 1. Domain Mapping
```bash
# Map custom domain to frontend
gcloud run domain-mappings create \
    --service=footybets-frontend \
    --domain=footybets.ai \
    --region=us-central1
```

### 2. SSL Certificate
Google Cloud automatically provisions SSL certificates for custom domains.

### 3. DNS Configuration
Add these DNS records to your domain provider:
```
Type: CNAME
Name: @
Value: ghs.googlehosted.com
```

## 📊 Monitoring & Logging

### 1. Enable Monitoring
```bash
gcloud services enable monitoring.googleapis.com
```

### 2. View Logs
```bash
# Backend logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=footybets-backend"

# Frontend logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=footybets-frontend"
```

### 3. Set up Alerts
```bash
# Create alerting policy
gcloud alpha monitoring policies create --policy-from-file=alert-policy.yaml
```

## 💰 Cost Optimization

### 1. Database Scaling
```bash
# Scale down during off-peak hours
gcloud sql instances patch footybets-db \
    --tier=db-f1-micro \
    --storage-size=10GB
```

### 2. Cloud Run Scaling
```bash
# Set minimum instances to 0 for cost savings
gcloud run services update footybets-backend \
    --min-instances=0 \
    --max-instances=5
```

## 🔒 Security Best Practices

### 1. Database Security
```bash
# Enable SSL connections
gcloud sql instances patch footybets-db \
    --require-ssl

# Create authorized networks
gcloud sql instances patch footybets-db \
    --authorized-networks=0.0.0.0/0
```

### 2. Service Account
```bash
# Create service account
gcloud iam service-accounts create footybets-sa \
    --display-name="FootyBets Service Account"

# Grant necessary permissions
gcloud projects add-iam-policy-binding footybets-ai \
    --member="serviceAccount:footybets-sa@footybets-ai.iam.gserviceaccount.com" \
    --role="roles/cloudsql.client"
```

## 🚨 Troubleshooting

### Common Issues:

1. **Build Failures**
   ```bash
   # Check build logs
   gcloud builds log [BUILD_ID]
   ```

2. **Database Connection Issues**
   ```bash
   # Test database connection
   gcloud sql connect footybets-db --user=footybets_user
   ```

3. **Service Not Starting**
   ```bash
   # Check service logs
   gcloud run services logs read footybets-backend --region=us-central1
   ```

4. **Memory Issues**
   ```bash
   # Increase memory allocation
   gcloud run services update footybets-backend \
       --memory=2Gi \
       --region=us-central1
   ```

## 📈 Scaling

### Auto-scaling Configuration
```bash
# Configure auto-scaling
gcloud run services update footybets-backend \
    --min-instances=1 \
    --max-instances=20 \
    --cpu-throttling \
    --concurrency=80
```

### Load Balancing
```bash
# Create load balancer
gcloud compute url-maps create footybets-lb \
    --default-service=footybets-frontend

# Create backend service
gcloud compute backend-services create footybets-backend \
    --global \
    --load-balancing-scheme=EXTERNAL_MANAGED
```

## 🎉 Success!

After deployment, your FootyBets.ai platform will be available at:
- **Frontend**: https://footybets-frontend-[hash]-uc.a.run.app
- **Backend API**: https://footybets-backend-[hash]-uc.a.run.app
- **Brownlow Content**: https://storage.googleapis.com/footybets-ai-static/brownlow-medal-predictions/

## 📞 Support

For issues with Google Cloud deployment:
- [Google Cloud Documentation](https://cloud.google.com/docs)
- [Cloud Run Troubleshooting](https://cloud.google.com/run/docs/troubleshooting)
- [Cloud SQL Support](https://cloud.google.com/sql/docs/support) 