# 🎯 Namecheap DNS Setup - Final Configuration

## ✅ Services Status
Both Google Cloud Run services are now working:
- **Frontend**: `https://footybets-frontend-818397187963.us-central1.run.app` ✅
- **Backend**: `https://footybets-backend-818397187963.us-central1.run.app` ✅

## 🔧 DNS Configuration Steps

### Step 1: Access Namecheap DNS
1. Log into your Namecheap account
2. Go to "Domain List"
3. Click "Manage" next to `footybets.ai`
4. Go to "Advanced DNS" tab

### Step 2: Delete All Existing Records
1. **IMPORTANT**: Delete ALL existing DNS records first
2. This ensures no conflicts with old configurations

### Step 3: Add URL Redirect (Recommended Method)
This is the simplest and most reliable method:

| Type | Host | Value | TTL |
|------|------|-------|-----|
| **URL Redirect** | **@** | `https://footybets-frontend-818397187963.us-central1.run.app` | **Automatic** |

### Step 4: Add CNAME Records for Subdomains
| Type | Host | Value | TTL |
|------|------|-------|-----|
| **CNAME** | **api** | `footybets-backend-818397187963.us-central1.run.app` | **Automatic** |
| **CNAME** | **www** | `footybets-frontend-818397187963.us-central1.run.app` | **Automatic** |

## 🎯 Expected Results
After DNS propagation (5-30 minutes):

- **`footybets.ai`** → Redirects to frontend
- **`www.footybets.ai`** → Frontend service
- **`api.footybets.ai`** → Backend API

## 🔍 Testing Commands
After setting up DNS, test with:

```bash
# Test main domain
curl -I https://footybets.ai

# Test subdomains
curl -I https://www.footybets.ai
curl -I https://api.footybets.ai
```

## ⚠️ Alternative: A Records Method
If URL Redirect doesn't work, use A records for the apex domain:

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

## 🚀 Ready to Deploy!
Your services are working perfectly. Just configure the DNS and you'll be live! 