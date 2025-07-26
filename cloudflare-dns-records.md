# 🌐 Cloudflare DNS Records for FootyBets.ai

## Quick Setup Reference

### Current Service URLs
- **Backend**: `https://footybets-backend-818397187963.us-central1.run.app`
- **Frontend**: `https://footybets-frontend-818397187963.us-central1.run.app`

### DNS Records Required by Google Cloud Run

**IMPORTANT**: These are the EXACT records required by Google Cloud Run for SSL certificate provisioning.

| Type | Name | Target | Proxy Status | TTL |
|------|------|--------|--------------|-----|
| A | @ | `216.239.32.21` | ❌ DNS Only | Auto |
| A | @ | `216.239.34.21` | ❌ DNS Only | Auto |
| A | @ | `216.239.36.21` | ❌ DNS Only | Auto |
| A | @ | `216.239.38.21` | ❌ DNS Only | Auto |
| AAAA | @ | `2001:4860:4802:32::15` | ❌ DNS Only | Auto |
| AAAA | @ | `2001:4860:4802:34::15` | ❌ DNS Only | Auto |
| AAAA | @ | `2001:4860:4802:36::15` | ❌ DNS Only | Auto |
| AAAA | @ | `2001:4860:4802:38::15` | ❌ DNS Only | Auto |

### Additional Records for Subdomains

| Type | Name | Target | Proxy Status | TTL |
|------|------|--------|--------------|-----|
| CNAME | api | `footybets-backend-818397187963.us-central1.run.app` | ✅ Proxied | Auto |
| CNAME | www | `footybets-frontend-818397187963.us-central1.run.app` | ✅ Proxied | Auto |

### Step-by-Step Instructions

1. **Log into Cloudflare Dashboard**
   - Go to: https://dash.cloudflare.com
   - Select domain: `footybets.ai`

2. **Navigate to DNS Settings**
   - Click "DNS" in left sidebar
   - Click "Records" tab

3. **Remove Existing Records**
   - Delete any existing A records for `@` (root domain)
   - Delete any existing AAAA records for `@` (root domain)

4. **Add Google Cloud Run Records**
   - Click "Add record" button
   - Add each A and AAAA record from the table above
   - **CRITICAL**: Set "Proxy status" to "DNS only" (gray cloud) for root domain records
   - This allows Google Cloud Run to handle SSL certificates

5. **Add Subdomain Records**
   - Add the CNAME records for `api` and `www` subdomains
   - These can use "Proxied" status (orange cloud)

### Expected URLs After Setup

- **Main Website**: https://footybets.ai (handled by Google Cloud Run)
- **API Endpoint**: https://api.footybets.ai (handled by Cloudflare)
- **www Redirect**: https://www.footybets.ai (handled by Cloudflare)

### Important Notes

⚠️ **Root Domain Must Be DNS Only**: The root domain (`@`) records MUST be set to "DNS only" (gray cloud) for Google Cloud Run SSL to work

🔒 **SSL Certificates**: Google Cloud Run will automatically provision SSL certificates once DNS is properly configured

🌍 **DNS Propagation**: Changes can take up to 24 hours to propagate globally

### Testing After Setup

1. Test main website: `https://footybets.ai`
2. Test API endpoint: `https://api.footybets.ai`
3. Verify www redirect works: `https://www.footybets.ai`

### Troubleshooting

If you see SSL errors after setup:
1. Verify all root domain records are "DNS only" (gray cloud)
2. Check that all 8 records (4 A + 4 AAAA) are present
3. Wait for DNS propagation (can take 24 hours)
4. Check Google Cloud Run domain mapping status: `gcloud beta run domain-mappings list --region=us-central1`

### Current Status

- ✅ Domain mapping created in Google Cloud Run
- ❌ DNS records need to be updated to match Google's requirements
- ❌ SSL certificate pending due to DNS configuration 