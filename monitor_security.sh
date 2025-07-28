#!/bin/bash

# Security Monitoring Script
PROJECT_ID="footybets-ai"
INSTANCE_NAME="footybets-db"

echo "🔍 Security Status Check:"
echo "========================"

# Check instance configuration
echo "📊 Instance security settings:"
gcloud sql instances describe $INSTANCE_NAME --project=$PROJECT_ID \
    --format="table(settings.ipConfiguration.requireSsl,settings.ipConfiguration.authorizedNetworks[].value)"

# Check SSL connections
echo ""
echo "🔒 SSL connection status:"
gcloud logging read "resource.type=cloudsql_database AND textPayload:ssl" \
    --project=$PROJECT_ID \
    --limit=3 \
    --format="table(timestamp,textPayload)"

# Check failed login attempts
echo ""
echo "🚨 Recent failed logins:"
gcloud logging read "resource.type=cloudsql_database AND textPayload:failed" \
    --project=$PROJECT_ID \
    --limit=5 \
    --format="table(timestamp,textPayload)"

# Check recent database connections
echo ""
echo "📊 Recent database connections:"
gcloud logging read "resource.type=cloudsql_database" \
    --project=$PROJECT_ID \
    --limit=5 \
    --format="table(timestamp,textPayload)"

echo ""
echo "✅ Security monitoring complete" 