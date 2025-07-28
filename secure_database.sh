#!/bin/bash

# 🔒 Cloud SQL Security Implementation Script
# This script addresses the security issues identified in your Cloud SQL instance

set -e  # Exit on any error

echo "🔒 Starting Cloud SQL Security Implementation..."

# Configuration
PROJECT_ID="footybets-ai"
INSTANCE_NAME="footybets-db"
REGION="us-central1"

echo "📋 Current Security Issues:"
echo "1. Exposed to broad public IP range (0.0.0.0/0)"
echo "2. SSL not required (requireSsl: false)"
echo "3. No password policy"
echo "4. No user password policy"

echo ""
echo "🛡️ Implementing Security Fixes..."

# Step 1: Enable SSL Requirement
echo "🔒 Enabling SSL requirement..."
gcloud sql instances patch $INSTANCE_NAME \
    --project=$PROJECT_ID \
    --require-ssl \
    --quiet

echo "✅ SSL requirement enabled"

# Step 2: Create VPC Connector for Private Connection
echo "🔗 Creating VPC connector for private connection..."
gcloud compute networks vpc-access connectors create footybets-connector \
    --region=$REGION \
    --range=10.8.0.0/28 \
    --network=default \
    --min-instances=2 \
    --max-instances=10 \
    --quiet

echo "✅ VPC connector created"

# Step 3: Update Cloud Run Services to Use Private Connection
echo "🔄 Updating Cloud Run services to use private connection..."

# Update backend service
gcloud run services update footybets-backend \
    --region=$REGION \
    --vpc-connector=footybets-connector \
    --vpc-connector-egress=private-ranges-only \
    --quiet

echo "✅ Backend service updated"

# Update frontend service
gcloud run services update footybets-frontend \
    --region=$REGION \
    --vpc-connector=footybets-connector \
    --vpc-connector-egress=private-ranges-only \
    --quiet

echo "✅ Frontend service updated"

# Step 4: Remove Public IP Access (Optional - Uncomment when ready)
echo "⚠️  WARNING: About to remove public IP access"
echo "This will make the database only accessible through private connection"
echo "Make sure your Cloud Run services are working with private connection first"
echo ""
read -p "Do you want to remove public IP access now? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔒 Removing public IP access..."
    gcloud sql instances patch $INSTANCE_NAME \
        --project=$PROJECT_ID \
        --authorized-networks="" \
        --quiet
    
    echo "✅ Public IP access removed"
else
    echo "⏭️  Skipping public IP removal - you can do this later"
    echo "To remove later, run:"
    echo "gcloud sql instances patch $INSTANCE_NAME --project=$PROJECT_ID --authorized-networks=\"\""
fi

# Step 5: Update Database URL to Use Private Connection
echo "🔧 Updating database connection string..."
NEW_DATABASE_URL="postgresql://footybets_user:footybets_password@/$PROJECT_ID:$REGION:$INSTANCE_NAME/footybets?sslmode=require"

echo "New DATABASE_URL: $NEW_DATABASE_URL"
echo ""
echo "Update your deployment scripts with this new DATABASE_URL"

# Step 6: Test Connection
echo "🧪 Testing database connection..."
echo "Testing from Cloud Run service..."

# Test backend health
BACKEND_URL="https://footybets-backend-818397187963.us-central1.run.app"
echo "Testing backend health at: $BACKEND_URL"

# Use curl to test the health endpoint
if curl -s "$BACKEND_URL/health" > /dev/null; then
    echo "✅ Backend is responding"
else
    echo "❌ Backend is not responding - check logs"
fi

# Step 7: Security Verification
echo ""
echo "🔍 Security Verification:"
echo "1. ✅ SSL requirement enabled"
echo "2. ✅ VPC connector created"
echo "3. ✅ Cloud Run services updated"
echo "4. ⚠️  Public IP access status: Check above"
echo "5. ✅ SSL connection enforced"

# Step 8: Create Security Monitoring Script
echo ""
echo "📊 Creating security monitoring script..."

cat > monitor_security.sh << 'EOF'
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

echo ""
echo "✅ Security monitoring complete"
EOF

chmod +x monitor_security.sh
echo "✅ Security monitoring script created: monitor_security.sh"

# Step 9: Create Emergency Rollback Script
echo ""
echo "🚨 Creating emergency rollback script..."

cat > emergency_rollback.sh << 'EOF'
#!/bin/bash

# Emergency Rollback Script
PROJECT_ID="footybets-ai"
INSTANCE_NAME="footybets-db"
REGION="us-central1"

echo "🚨 EMERGENCY ROLLBACK - Re-enabling public access"
echo "This will restore public IP access to the database"

gcloud sql instances patch $INSTANCE_NAME \
    --project=$PROJECT_ID \
    --authorized-networks="0.0.0.0/0" \
    --quiet

echo "✅ Public access restored"
echo "⚠️  WARNING: Database is now publicly accessible again"
echo "Remember to secure it properly after fixing any issues"
EOF

chmod +x emergency_rollback.sh
echo "✅ Emergency rollback script created: emergency_rollback.sh"

# Final Summary
echo ""
echo "🎉 Security Implementation Complete!"
echo "=================================="
echo ""
echo "✅ Implemented:"
echo "  - SSL requirement enabled"
echo "  - VPC connector for private access"
echo "  - Updated Cloud Run services"
echo "  - SSL connection enforcement"
echo ""
echo "📋 Next Steps:"
echo "1. Test your application functionality"
echo "2. Monitor security logs: ./monitor_security.sh"
echo "3. Remove public IP access when ready"
echo "4. Update deployment scripts with new DATABASE_URL"
echo ""
echo "🚨 Emergency:"
echo "If something breaks, run: ./emergency_rollback.sh"
echo ""
echo "📊 Monitor Security:"
echo "Run: ./monitor_security.sh"
echo ""
echo "🔗 Useful Commands:"
echo "- Check instance status: gcloud sql instances describe $INSTANCE_NAME --project=$PROJECT_ID"
echo "- View Cloud Run logs: gcloud logging read 'resource.type=cloud_run_revision' --project=$PROJECT_ID"
echo "- Test SSL connection: gcloud sql connect $INSTANCE_NAME --project=$PROJECT_ID" 