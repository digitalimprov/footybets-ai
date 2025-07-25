# 🔧 DNS Troubleshooting: "Content Cannot Be Displayed" Fix

## 🚨 Problem Identified

Your domain `footybets.ai` is currently pointing to `192.64.119.183` instead of Google Cloud Run IPs.

**Current DNS lookup result:**
```
footybets.ai → 192.64.119.183 (❌ Wrong IP)
```

**Should be pointing to Google Cloud IPs:**
```
footybets.ai → 34.143.72.2, 34.143.73.2, etc. (✅ Correct IPs)
```

## 🔧 Solution: Update DNS Records in Namecheap

### Step 1: Check Current DNS Records
1. Go to Namecheap Dashboard
2. Domain List → footybets.ai → Manage → Advanced DNS
3. Look at "Host Records" section
4. **Delete any existing records** that point to wrong IPs

### Step 2: Add Correct A Records
Add these 8 A records for the apex domain:

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

### Step 3: Add CNAME Records
Add these CNAME records for subdomains:

| Type | Host | Value | TTL |
|------|------|-------|-----|
| CNAME | api | `footybets-backend-wlbnzevhqa-uc.a.run.app` | Automatic |
| CNAME | www | `footybets-frontend-wlbnzevhqa-uc.a.run.app` | Automatic |

### Step 4: Save and Wait
1. Click "Save All Changes"
2. Wait 15-30 minutes for DNS propagation

## 🧪 Testing Commands

After updating DNS, test with:

```bash
# Test main domain
nslookup footybets.ai

# Test subdomains
nslookup api.footybets.ai
nslookup www.footybets.ai

# Test direct access
curl -I https://footybets.ai
```

## ✅ Expected Results

After DNS propagation, you should see:
```
footybets.ai → 34.143.72.2 (or other Google Cloud IPs)
api.footybets.ai → footybets-backend-wlbnzevhqa-uc.a.run.app
www.footybets.ai → footybets-frontend-wlbnzevhqa-uc.a.run.app
```

## 🆘 Alternative: URL Redirect Method

If A records still don't work, use URL Redirect:

1. **Delete all existing records**
2. **Add one URL Redirect record:**
   - Type: URL Redirect
   - Host: @
   - Value: `https://footybets-frontend-wlbnzevhqa-uc.a.run.app`
   - TTL: Automatic

## 🔍 Common Issues

### Issue 1: Old DNS Records Still Active
- **Solution**: Delete all existing records first
- **Check**: Look for any records pointing to `192.64.119.183`

### Issue 2: DNS Propagation Delay
- **Solution**: Wait 15-30 minutes
- **Test**: Use `nslookup footybets.ai` to verify

### Issue 3: Wrong Service URLs
- **Current Frontend**: `footybets-frontend-wlbnzevhqa-uc.a.run.app`
- **Current Backend**: `footybets-backend-wlbnzevhqa-uc.a.run.app`

## 🎯 Quick Fix Summary

1. **Delete all existing DNS records** in Namecheap
2. **Add 8 A records** with Google Cloud IPs (34.143.72.2 - 34.143.79.2)
3. **Add 2 CNAME records** for api and www subdomains
4. **Save changes** and wait 15-30 minutes
5. **Test with nslookup** to verify propagation

Your website should then be accessible at `https://footybets.ai`! 