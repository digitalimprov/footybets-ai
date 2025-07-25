# 🔧 Namecheap DNS Troubleshooting Guide

## Common DNS Errors and Solutions

### ❌ Error: "Invalid CNAME Record"
**Problem**: Namecheap doesn't allow CNAME records for apex domain (@)

**Solution**: Use A records instead for the apex domain

### ❌ Error: "Invalid Host Value"
**Problem**: Incorrect format for the host field

**Solution**: Use exact values as shown below

### ❌ Error: "Invalid Target Value"
**Problem**: Target URL format is incorrect

**Solution**: Remove the `https://` protocol from the target

## ✅ Correct DNS Records for Namecheap

### Option 1: A Records for Apex Domain (Recommended)

| Type | Host | Value | TTL |
|------|------|-------|-----|
| A | @ | `34.143.72.2` | Automatic |
| A | @ | `34.143.73.2` | Automatic |
| A | @ | `34.143.74.2` | Automatic |
| A | @ | `34.143.75.2` | Automatic |
| A | @ | `34.143.76.2` | Automatic |
| A | @ | `34.143.77.2` | Automatic |
| A | @ | `34.143.78.2` | Automatic |
| A | @ | `34.143.79.2` | Automatic |
| CNAME | api | `footybets-backend-818397187963.us-central1.run.app` | Automatic |
| CNAME | www | `footybets-frontend-818397187963.us-central1.run.app` | Automatic |

### Option 2: URL Redirect for Apex Domain

| Type | Host | Value | TTL |
|------|------|-------|-----|
| URL Redirect | @ | `https://footybets-frontend-818397187963.us-central1.run.app` | Automatic |
| CNAME | api | `footybets-backend-818397187963.us-central1.run.app` | Automatic |
| CNAME | www | `footybets-frontend-818397187963.us-central1.run.app` | Automatic |

## 🔍 Step-by-Step Fix

1. **Go to Namecheap Advanced DNS**
   - Login to Namecheap
   - Go to Domain List → footybets.ai → Manage → Advanced DNS

2. **Remove any existing incorrect records**
   - Delete any CNAME records with host "@"
   - Delete any records with "https://" in the value field

3. **Add the correct records**
   - Use Option 1 (A records) for best performance
   - Or use Option 2 (URL redirect) for simpler setup

4. **Save and wait**
   - Click "Save All Changes"
   - Wait 15-30 minutes for propagation

## 🧪 Testing Your Setup

After adding the records, test with:

```bash
# Test main domain
nslookup footybets.ai

# Test API subdomain
nslookup api.footybets.ai

# Test www subdomain
nslookup www.footybets.ai
```

## ⚠️ Important Notes

- **Never include "https://" in DNS record values**
- **Apex domains (@) cannot use CNAME records in most DNS providers**
- **Use A records or URL redirects for apex domains**
- **CNAME records work fine for subdomains (api, www)**

## 🆘 Still Having Issues?

If you're still getting errors:

1. **Screenshot the exact error message**
2. **Check Namecheap's DNS documentation**
3. **Contact Namecheap support**
4. **Consider using Cloudflare (free) for easier DNS management** 