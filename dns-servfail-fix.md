# 🔧 DNS SERVFAIL Error Fix

## 🚨 Problem: SERVFAIL Error

Your domain `footybets.ai` is returning SERVFAIL errors, which means there's a DNS configuration issue in Namecheap.

**Error:**
```
** server can't find footybets.ai: SERVFAIL
```

## 🔍 Root Cause Analysis

SERVFAIL errors typically occur when:
1. **DNS records are misconfigured**
2. **Conflicting DNS records**
3. **Invalid record types for the domain**
4. **DNS propagation issues**

## 🔧 Step-by-Step Fix

### Step 1: Check Current DNS Records in Namecheap

1. **Go to Namecheap Dashboard**
   - Login to: https://ap.www.namecheap.com/myaccount/login/
   - Go to Domain List → footybets.ai → Manage → Advanced DNS

2. **Review Current Records**
   - Look at all records in "Host Records" section
   - **Delete ALL existing records** (we'll start fresh)

### Step 2: Add Records One by One

**Start with a simple test record:**

1. **Add one A record first:**
   - Type: A Record
   - Host: @
   - Value: `34.143.72.2`
   - TTL: Automatic
   - Click Save

2. **Test this single record:**
   ```bash
   nslookup footybets.ai 8.8.8.8
   ```

### Step 3: If Single Record Works, Add the Rest

If the single A record resolves correctly, add the remaining records:

**Add 7 more A records:**
- A | @ | `34.143.73.2` | Automatic
- A | @ | `34.143.74.2` | Automatic
- A | @ | `34.143.75.2` | Automatic
- A | @ | `34.143.76.2` | Automatic
- A | @ | `34.143.77.2` | Automatic
- A | @ | `34.143.78.2` | Automatic
- A | @ | `34.143.79.2` | Automatic

**Add CNAME records:**
- CNAME | api | `footybets-backend-wlbnzevhqa-uc.a.run.app` | Automatic
- CNAME | www | `footybets-frontend-wlbnzevhqa-uc.a.run.app` | Automatic

### Step 4: Alternative - Use URL Redirect

If A records continue to cause SERVFAIL errors:

1. **Delete all A records**
2. **Add one URL Redirect record:**
   - Type: URL Redirect
   - Host: @
   - Value: `https://footybets-frontend-wlbnzevhqa-uc.a.run.app`
   - TTL: Automatic

## 🧪 Testing After Each Step

```bash
# Test main domain
nslookup footybets.ai 8.8.8.8

# Test subdomains
nslookup api.footybets.ai 8.8.8.8
nslookup www.footybets.ai 8.8.8.8

# Test direct access
curl -I https://footybets.ai
```

## 🚨 Common SERVFAIL Causes

### Cause 1: Invalid A Record Configuration
- **Solution**: Make sure Host is exactly `@` (not "footybets.ai")
- **Solution**: Ensure IP addresses are valid Google Cloud IPs

### Cause 2: Conflicting Record Types
- **Solution**: Don't mix A records with CNAME for same host
- **Solution**: Delete all records and start fresh

### Cause 3: DNS Propagation Issues
- **Solution**: Wait 15-30 minutes between changes
- **Solution**: Use different DNS servers for testing

### Cause 4: Namecheap DNS Issues
- **Solution**: Contact Namecheap support
- **Solution**: Consider switching to Cloudflare DNS

## 🆘 Emergency Fix: Cloudflare DNS

If Namecheap DNS continues to have issues:

1. **Sign up for free Cloudflare account**
2. **Add footybets.ai to Cloudflare**
3. **Update nameservers to Cloudflare's**
4. **Configure DNS records in Cloudflare**

## 📞 Contact Namecheap Support

If the issue persists:
- **Email**: support@namecheap.com
- **Live Chat**: Available on Namecheap website
- **Reference**: SERVFAIL error for footybets.ai

## 🎯 Quick Diagnostic Commands

```bash
# Test with different DNS servers
nslookup footybets.ai 8.8.8.8
nslookup footybets.ai 1.1.1.1
nslookup footybets.ai 208.67.222.222

# Check domain registration
whois footybets.ai

# Test direct IP access
curl -I https://34.143.72.2
``` 