# 🌐 Namecheap DNS Records for FootyBets.ai

## Quick Setup Reference

### Current Service URLs
- **Backend**: `https://footybets-backend-818397187963.us-central1.run.app`
- **Frontend**: `https://footybets-frontend-818397187963.us-central1.run.app`

### DNS Records Required by Google Cloud Run

**IMPORTANT**: These are the EXACT records required by Google Cloud Run for SSL certificate provisioning.

| Type | Host | Value | TTL |
|------|------|-------|-----|
| A | @ | `216.239.32.21` | 30 min |
| A | @ | `216.239.34.21` | 30 min |
| A | @ | `216.239.36.21` | 30 min |
| A | @ | `216.239.38.21` | 30 min |
| AAAA | @ | `2001:4860:4802:32::15` | 30 min |
| AAAA | @ | `2001:4860:4802:34::15` | 30 min |
| AAAA | @ | `2001:4860:4802:36::15` | 30 min |
| AAAA | @ | `2001:4860:4802:38::15` | 30 min |

### Additional Records for Subdomains

| Type | Host | Value | TTL |
|------|------|-------|-----|
| CNAME | api | `footybets-backend-818397187963.us-central1.run.app` | 30 min |
| CNAME | www | `footybets-frontend-818397187963.us-central1.run.app` | 30 min |

### Step-by-Step Instructions

1. **Log into Namecheap Dashboard**
   - Go to: https://ap.www.namecheap.com/Domains/DomainControlPanel
   - Select domain: `footybets.ai`

2. **Navigate to DNS Settings**
   - Click "Manage" next to your domain
   - Click "Advanced DNS" tab

3. **Remove Existing Records**
   - Delete any existing A records for `@` (root domain)
   - Delete any existing AAAA records for `@` (root domain)

4. **Add Google Cloud Run Records**
   - Click "Add New Record" button
   - Add each A and AAAA record from the table above:
     - **Type**: A or AAAA
     - **Host**: @ (leave empty for root domain)
     - **Value**: The IP address from the table
     - **TTL**: 30 min

5. **Add Subdomain Records**
   - Add the CNAME records for `api` and `www` subdomains:
     - **Type**: CNAME
     - **Host**: api or www
     - **Value**: The Cloud Run URL
     - **TTL**: 30 min

### Expected URLs After Setup

- **Main Website**: https://footybets.ai (handled by Google Cloud Run)
- **API Endpoint**: https://api.footybets.ai (handled by Google Cloud Run)
- **www Redirect**: https://www.footybets.ai (handled by Google Cloud Run)

### Important Notes

⚠️ **Root Domain Records**: The root domain (`@`) records are critical for Google Cloud Run SSL to work

🔒 **SSL Certificates**: Google Cloud Run will automatically provision SSL certificates once DNS is properly configured

🌍 **DNS Propagation**: Changes can take up to 24 hours to propagate globally

### Testing After Setup

1. Test main website: `https://footybets.ai`
2. Test API endpoint: `https://api.footybets.ai`
3. Verify www redirect works: `https://www.footybets.ai`

### Troubleshooting

If you see SSL errors after setup:
1. Verify all 8 records (4 A + 4 AAAA) are present for root domain
2. Check that TTL is set to 30 min for faster propagation
3. Wait for DNS propagation (can take 24 hours)
4. Check Google Cloud Run domain mapping status: `gcloud beta run domain-mappings list --region=us-central1`

### Current Status

- ✅ Domain mapping created in Google Cloud Run
- ❌ DNS records need to be updated to match Google's requirements
- ❌ SSL certificate pending due to DNS configuration

### Namecheap-Specific Notes

- Namecheap doesn't have proxy options like Cloudflare, so all records are DNS-only by default
- This is actually better for Google Cloud Run as it allows direct SSL certificate provisioning
- The 30-minute TTL will help with faster DNS propagation 