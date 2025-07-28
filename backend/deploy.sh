#!/bin/bash

# Production Deployment Script for FootyBets Backend
# This script ensures PostgreSQL is always used in production

set -e

echo "🚀 Deploying FootyBets Backend to Cloud Run..."

# Production environment variables
export ENVIRONMENT=production

# Check for required environment variables
if [ -z "$FOOTYBETS_USER_PASSWORD" ]; then
    echo "❌ Error: FOOTYBETS_USER_PASSWORD environment variable not set"
    echo "Please run: export FOOTYBETS_USER_PASSWORD='your-footybets-user-password'"
    exit 1
fi

export DATABASE_URL="postgresql://footybets_user:${FOOTYBETS_USER_PASSWORD}@34.69.151.218:5432/footybets"
export SECRET_KEY="fW0a6njr3OV6P3L-mc2fz5Avby7Bk8F6eOqf5wIxRdA"
export API_SECRET_KEY="1wwutzADTGrzDA5-FVPUXJnI-Xoky9wrGSmUgQf1hz8"

# Deploy to Cloud Run with PostgreSQL configuration
gcloud run deploy footybets-backend \
  --source . \
  --region=us-central1 \
  --allow-unauthenticated \
  --set-env-vars="ENVIRONMENT=production,DATABASE_URL=postgresql://footybets_user:${FOOTYBETS_USER_PASSWORD}@34.69.151.218:5432/footybets,SECRET_KEY=fW0a6njr3OV6P3L-mc2fz5Avby7Bk8F6eOqf5wIxRdA,API_SECRET_KEY=1wwutzADTGrzDA5-FVPUXJnI-Xoky9wrGSmUgQf1hz8" \
  --memory=2Gi \
  --cpu=2 \
  --timeout=300 \
  --concurrency=80

echo "✅ Backend deployed successfully!"
echo "🌐 Service URL: https://footybets-backend-818397187963.us-central1.run.app"
echo "📊 Health Check: https://footybets-backend-818397187963.us-central1.run.app/health" 