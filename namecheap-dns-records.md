# 🌐 Namecheap DNS Records for FootyBets.ai

## Quick Setup Reference

### Current Service URLs
- **Backend**: `footybets-backend-818397187963.us-central1.run.app`
- **Frontend**: `footybets-frontend-818397187963.us-central1.run.app`

### DNS Records to Add in Namecheap

| Type | Host | Value | TTL |
|------|------|-------|-----|
| CNAME | @ | `footybets-frontend-818397187963.us-central1.run.app` | Automatic |
| CNAME | api | `footybets-backend-818397187963.us-central1.run.app` | Automatic |
| CNAME | www | `footybets-frontend-818397187963.us-central1.run.app` | Automatic |

### Step-by-Step Instructions

1. **Log into Namecheap**
   - Go to: https://ap.www.namecheap.com/myaccount/login/
   - Sign in to your account

2. **Access Domain Management**
   - Click "Domain List" in left sidebar
   - Find `footybets.ai`
   - Click "Manage" next to your domain

3. **Go to DNS Settings**
   - Click "Advanced DNS" tab
   - Look for "Host Records" section

4. **Add Records**
   - Click "Add New Record" button
   - Add each record from the table above
   - Make sure TTL is set to "Automatic"

5. **Optional: Add URL Redirect**
   - Go to "URL Redirect Records" section
   - Add: `www.footybets.ai` → `footybets.ai`

6. **Save Changes**
   - Click "Save All Changes" button

### Expected URLs After Setup

- **Main Website**: https://footybets.ai
- **API Endpoint**: https://api.footybets.ai  
- **www Redirect**: https://www.footybets.ai (redirects to footybets.ai)

### Important Notes

⚠️ **DNS Propagation**: Changes can take up to 24 hours to propagate globally

🔒 **SSL**: Google Cloud Run automatically provides SSL certificates

🌍 **Performance**: Namecheap DNS doesn't provide CDN or DDoS protection

### Testing After Setup

1. Test main website: `https://footybets.ai`
2. Test API endpoint: `https://api.footybets.ai`
3. Verify www redirect works: `https://www.footybets.ai`

### Troubleshooting

If you see errors after setup:
1. Check that all CNAME records are correct
2. Verify the target URLs are accurate
3. Wait for DNS propagation (can take 24 hours)
4. Check Namecheap's status page for any issues

### Optional: Add Cloudflare CDN

For better performance and security:
1. Sign up for free Cloudflare account
2. Add your domain to Cloudflare
3. Update nameservers to Cloudflare's
4. Get free CDN, DDoS protection, and enhanced SSL 