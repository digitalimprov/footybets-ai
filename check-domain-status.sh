#!/bin/bash

# FootyBets.ai Domain Status Checker
# This script helps troubleshoot domain mapping and SSL issues

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 FootyBets.ai Domain Status Check${NC}"
echo "=========================================="

# Check if gcloud is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${RED}❌ Not authenticated with Google Cloud${NC}"
    exit 1
fi

# Check Cloud Run services
echo -e "${BLUE}📊 Checking Cloud Run services...${NC}"
gcloud run services list --region=us-central1 --format="table(metadata.name,status.url,status.conditions[0].status)"

# Check domain mapping status
echo -e "\n${BLUE}🌐 Checking domain mapping...${NC}"
gcloud beta run domain-mappings list --region=us-central1 --format="table(domain,service,status.conditions[0].type,status.conditions[0].status,status.conditions[0].message)"

# Check DNS resolution
echo -e "\n${BLUE}🔍 Checking DNS resolution...${NC}"
echo "footybets.ai resolves to:"
dig +short footybets.ai

# Test HTTPS connection
echo -e "\n${BLUE}🔒 Testing HTTPS connection...${NC}"
if curl -s -I https://footybets.ai > /dev/null 2>&1; then
    echo -e "${GREEN}✅ HTTPS connection successful${NC}"
else
    echo -e "${RED}❌ HTTPS connection failed${NC}"
    echo "This indicates SSL certificate issues"
fi

# Test direct Cloud Run URL
echo -e "\n${BLUE}🔗 Testing direct Cloud Run URL...${NC}"
if curl -s -I https://footybets-frontend-818397187963.us-central1.run.app > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Direct Cloud Run URL works${NC}"
else
    echo -e "${RED}❌ Direct Cloud Run URL failed${NC}"
fi

echo -e "\n${BLUE}📋 Next Steps:${NC}"
echo "1. Update DNS records in Namecheap as per namecheap-dns-records.md"
echo "2. Wait for DNS propagation (up to 24 hours)"
echo "3. Run this script again to check status"
echo ""
echo -e "${YELLOW}💡 Tip: Make sure all 8 DNS records (4 A + 4 AAAA) are configured for the root domain${NC}" 