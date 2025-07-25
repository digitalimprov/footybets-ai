# 🌐 Cloudflare DNS Records for FootyBets.ai

## Quick Setup Reference

### Current Service URLs
- **Backend**: `https://footybets-backend-818397187963.us-central1.run.app`
- **Frontend**: `https://footybets-frontend-818397187963.us-central1.run.app`

### DNS Records to Add

| Type | Name | Target | Proxy Status | TTL |
|------|------|--------|--------------|-----|
| CNAME | @ | `footybets-frontend-818397187963.us-central1.run.app` | ✅ Proxied | Auto |
| CNAME | api | `footybets-backend-818397187963.us-central1.run.app` | ✅ Proxied | Auto |
| CNAME | www | `footybets-frontend-818397187963.us-central1.run.app` | ✅ Proxied | Auto |

### Step-by-Step Instructions

1. **Log into Cloudflare Dashboard**
   - Go to: https://dash.cloudflare.com
   - Select domain: `footybets.ai`

2. **Navigate to DNS Settings**
   - Click "DNS" in left sidebar
   - Click "Records" tab

3. **Add Records**
   - Click "Add record" button
   - Add each record from the table above
   - Make sure "Proxy status" is set to "Proxied" (orange cloud)

### Expected URLs After Setup

- **Main Website**: https://footybets.ai
- **API Endpoint**: https://api.footybets.ai  
- **www Redirect**: https://www.footybets.ai (redirects to footybets.ai)

### Important Notes

⚠️ **DNS Propagation**: Changes can take up to 24 hours to propagate globally

🔒 **Security**: The orange cloud (proxy) provides DDoS protection and caching

🌍 **SSL**: Cloudflare will automatically provide SSL certificates

### Testing After Setup

1. Test main website: `https://footybets.ai`
2. Test API endpoint: `https://api.footybets.ai`
3. Verify www redirect works: `https://www.footybets.ai`

### Troubleshooting

If you see errors after setup:
1. Check that all records have "Proxied" status (orange cloud)
2. Verify the target URLs are correct
3. Wait for DNS propagation (can take 24 hours)
4. Check Cloudflare's status page for any issues 