#!/bin/bash

# FootyBets.ai Namecheap DNS Configuration Script
# This script helps you configure Namecheap DNS to point to your Google Cloud Run services

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

echo -e "${BLUE}🌐 FootyBets.ai Namecheap DNS Configuration${NC}"
echo "=================================================="

echo -e "${BLUE}📋 Current Service URLs:${NC}"
echo -e "  Backend: ${GREEN}$BACKEND_URL${NC}"
echo -e "  Frontend: ${GREEN}$FRONTEND_URL${NC}"
echo ""

echo -e "${BLUE}🔧 Namecheap DNS Configuration Steps:${NC}"
echo "=================================================="
echo ""
echo -e "${YELLOW}1. Log into Namecheap Dashboard${NC}"
echo "   • Go to: https://ap.www.namecheap.com/myaccount/login/"
echo "   • Sign in to your Namecheap account"
echo ""
echo -e "${YELLOW}2. Access Domain Management${NC}"
echo "   • Click on 'Domain List' in the left sidebar"
echo "   • Find your domain: $DOMAIN"
echo "   • Click 'Manage' next to your domain"
echo ""
echo -e "${YELLOW}3. Go to DNS Settings${NC}"
echo "   • Click on 'Advanced DNS' tab"
echo "   • You'll see the 'Host Records' section"
echo ""
echo -e "${YELLOW}4. Configure DNS Records${NC}"
echo "   Add the following records:"
echo ""
echo -e "${GREEN}📝 Main Website (Apex Domain):${NC}"
echo "   Type: CNAME Record"
echo "   Host: @"
echo "   Value: $FRONTEND_URL"
echo "   TTL: Automatic"
echo ""
echo -e "${GREEN}📝 API Subdomain:${NC}"
echo "   Type: CNAME Record"
echo "   Host: api"
echo "   Value: $BACKEND_URL"
echo "   TTL: Automatic"
echo ""
echo -e "${GREEN}📝 www Subdomain:${NC}"
echo "   Type: CNAME Record"
echo "   Host: www"
echo "   Value: $FRONTEND_URL"
echo "   TTL: Automatic"
echo ""
echo -e "${YELLOW}5. URL Redirect Records (Optional)${NC}"
echo "   • Go to 'URL Redirect Records' section"
echo "   • Add redirect: www.$DOMAIN → $DOMAIN"
echo "   • This ensures www redirects to the main domain"
echo ""
echo -e "${YELLOW}6. Save Changes${NC}"
echo "   • Click 'Save All Changes' button"
echo "   • Wait for confirmation message"
echo ""

echo -e "${BLUE}🔍 DNS Record Summary:${NC}"
echo "=================================================="
echo "| Type | Host | Value | TTL |"
echo "|------|------|-------|-----|"
echo "| CNAME | @ | $FRONTEND_URL | Auto |"
echo "| CNAME | api | $BACKEND_URL | Auto |"
echo "| CNAME | www | $FRONTEND_URL | Auto |"
echo ""

echo -e "${BLUE}🌍 Expected URLs After Configuration:${NC}"
echo "=================================================="
echo -e "  Main Website: ${GREEN}https://$DOMAIN${NC}"
echo -e "  API Endpoint: ${GREEN}https://api.$DOMAIN${NC}"
echo -e "  www Redirect: ${GREEN}https://www.$DOMAIN${NC} (redirects to $DOMAIN)"
echo ""

echo -e "${BLUE}🔒 SSL Certificate Setup${NC}"
echo "=================================================="
echo "Since you're using Namecheap DNS (not Cloudflare), you'll need to:"
echo ""
echo -e "${YELLOW}Option 1: Google Cloud SSL (Recommended)${NC}"
echo "• Google Cloud Run automatically provides SSL certificates"
echo "• Your services will be accessible via HTTPS"
echo ""
echo -e "${YELLOW}Option 2: Namecheap SSL Certificate${NC}"
echo "• Purchase SSL certificate from Namecheap"
echo "• Install it on your Google Cloud Run services"
echo "• More complex setup required"
echo ""

echo -e "${BLUE}⚡ Performance Considerations${NC}"
echo "=================================================="
echo "• Namecheap DNS doesn't provide CDN or DDoS protection"
echo "• Consider using Cloudflare as a free CDN layer"
echo "• Google Cloud Run provides good performance globally"
echo ""

echo -e "${YELLOW}⚠️  Important Notes:${NC}"
echo "=================================================="
echo "1. DNS changes can take up to 24 hours to propagate globally"
echo "2. Namecheap DNS doesn't provide proxy protection like Cloudflare"
echo "3. Your Google Cloud Run services will be directly accessible"
echo "4. SSL certificates are handled by Google Cloud Run automatically"
echo ""

echo -e "${GREEN}✅ After completing these steps:${NC}"
echo "=================================================="
echo "• Your website will be accessible at https://$DOMAIN"
echo "• Your API will be accessible at https://api.$DOMAIN"
echo "• SSL certificates will be managed by Google Cloud Run"
echo "• DNS will be managed by Namecheap"
echo ""

echo -e "${BLUE}🔧 Next Steps After DNS Setup:${NC}"
echo "=================================================="
echo "1. Update your frontend environment variables to use the new API URL"
echo "2. Test all functionality with the new domain"
echo "3. Consider setting up Cloudflare as a free CDN layer"
echo "4. Set up monitoring and analytics"
echo ""

echo -e "${BLUE}🚀 Optional: Add Cloudflare CDN Layer${NC}"
echo "=================================================="
echo "For better performance and security, consider:"
echo "1. Sign up for free Cloudflare account"
echo "2. Add your domain to Cloudflare"
echo "3. Update nameservers to Cloudflare's"
echo "4. Get free CDN, DDoS protection, and SSL"
echo ""

echo -e "${GREEN}🎉 Your FootyBets.ai will be live at https://$DOMAIN!${NC}" 