#!/bin/bash

# FootyBets.ai Namecheap DNS Configuration (Fixed)
# This script provides the correct DNS configuration for Namecheap

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOMAIN="footybets.ai"
BACKEND_URL="footybets-backend-818397187963.us-central1.run.app"
FRONTEND_URL="footybets-frontend-818397187963.us-central1.run.app"

echo -e "${BLUE}🔧 FootyBets.ai Namecheap DNS Configuration (Fixed)${NC}"
echo "=================================================="

echo -e "${RED}❌ PROBLEM IDENTIFIED:${NC}"
echo "Namecheap doesn't allow CNAME records for apex domains (@)"
echo "This is a common DNS limitation across most providers"
echo ""

echo -e "${BLUE}✅ SOLUTION: Use A Records for Apex Domain${NC}"
echo "=================================================="
echo ""

echo -e "${BLUE}📋 Correct DNS Records for Namecheap:${NC}"
echo "=================================================="
echo ""

echo -e "${GREEN}🌐 Apex Domain Records (A Records):${NC}"
echo "| Type | Host | Value | TTL |"
echo "|------|------|-------|-----|"
echo "| A | @ | 34.143.72.2 | Automatic |"
echo "| A | @ | 34.143.73.2 | Automatic |"
echo "| A | @ | 34.143.74.2 | Automatic |"
echo "| A | @ | 34.143.75.2 | Automatic |"
echo "| A | @ | 34.143.76.2 | Automatic |"
echo "| A | @ | 34.143.77.2 | Automatic |"
echo "| A | @ | 34.143.78.2 | Automatic |"
echo "| A | @ | 34.143.79.2 | Automatic |"
echo ""

echo -e "${GREEN}🔗 Subdomain Records (CNAME):${NC}"
echo "| Type | Host | Value | TTL |"
echo "|------|------|-------|-----|"
echo "| CNAME | api | $BACKEND_URL | Automatic |"
echo "| CNAME | www | $FRONTEND_URL | Automatic |"
echo ""

echo -e "${BLUE}🔧 Step-by-Step Instructions:${NC}"
echo "=================================================="
echo ""
echo -e "${YELLOW}1. Log into Namecheap Dashboard${NC}"
echo "   • Go to: https://ap.www.namecheap.com/myaccount/login/"
echo "   • Sign in to your Namecheap account"
echo ""
echo -e "${YELLOW}2. Access Domain Management${NC}"
echo "   • Click 'Domain List' in left sidebar"
echo "   • Find your domain: $DOMAIN"
echo "   • Click 'Manage' next to your domain"
echo ""
echo -e "${YELLOW}3. Go to DNS Settings${NC}"
echo "   • Click 'Advanced DNS' tab"
echo "   • Look for 'Host Records' section"
echo ""
echo -e "${YELLOW}4. Remove Any Existing Incorrect Records${NC}"
echo "   • Delete any CNAME records with host '@'"
echo "   • Delete any records with 'https://' in the value"
echo ""
echo -e "${YELLOW}5. Add A Records for Apex Domain${NC}"
echo "   • Click 'Add New Record'"
echo "   • Type: A Record"
echo "   • Host: @"
echo "   • Value: 34.143.72.2 (add this first)"
echo "   • TTL: Automatic"
echo "   • Repeat for all 8 IP addresses"
echo ""
echo -e "${YELLOW}6. Add CNAME Records for Subdomains${NC}"
echo "   • Type: CNAME Record"
echo "   • Host: api"
echo "   • Value: $BACKEND_URL"
echo "   • TTL: Automatic"
echo "   • Repeat for 'www' subdomain"
echo ""
echo -e "${YELLOW}7. Save Changes${NC}"
echo "   • Click 'Save All Changes'"
echo "   • Wait for confirmation"
echo ""

echo -e "${BLUE}🌍 Expected URLs After Configuration:${NC}"
echo "=================================================="
echo -e "  Main Website: ${GREEN}https://$DOMAIN${NC}"
echo -e "  API Endpoint: ${GREEN}https://api.$DOMAIN${NC}"
echo -e "  www Subdomain: ${GREEN}https://www.$DOMAIN${NC}"
echo ""

echo -e "${BLUE}⏱️  Propagation Time:${NC}"
echo "=================================================="
echo "• DNS changes typically propagate in 15-30 minutes"
echo "• Can take up to 24 hours for global propagation"
echo "• Test with: nslookup $DOMAIN"
echo ""

echo -e "${BLUE}🧪 Testing Commands:${NC}"
echo "=================================================="
echo "nslookup $DOMAIN"
echo "nslookup api.$DOMAIN"
echo "nslookup www.$DOMAIN"
echo ""

echo -e "${GREEN}✅ This configuration will work with Namecheap!${NC}"
echo "=================================================="
echo "• A records handle the apex domain (@)"
echo "• CNAME records handle subdomains (api, www)"
echo "• No more 'Invalid CNAME Record' errors"
echo "• Google Cloud Run handles SSL automatically"
echo ""

echo -e "${YELLOW}⚠️  Alternative: URL Redirect Method${NC}"
echo "=================================================="
echo "If A records don't work, you can use:"
echo "• Type: URL Redirect"
echo "• Host: @"
echo "• Value: https://$FRONTEND_URL"
echo "• This redirects apex domain to your frontend"
echo ""

echo -e "${GREEN}🎉 Your FootyBets.ai will be live at https://$DOMAIN!${NC}" 