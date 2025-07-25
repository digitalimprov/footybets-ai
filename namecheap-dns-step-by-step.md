# 📍 Exact Steps: Where to Add A Records in Namecheap

## 🎯 Step-by-Step with Screenshots

### Step 1: Login to Namecheap
- Go to: https://ap.www.namecheap.com/myaccount/login/
- Sign in with your Namecheap account

### Step 2: Find Your Domain
- Click **"Domain List"** in the left sidebar
- Find **"footybets.ai"** in your domain list
- Click the **"Manage"** button next to it

### Step 3: Go to DNS Settings
- In the domain management page, click the **"Advanced DNS"** tab
- You'll see a section called **"Host Records"**

### Step 4: Add A Records (Exact Location)

**Look for the "Host Records" section** - it will look like this:

```
Host Records
Type    | Host | Value        | TTL
--------|------|--------------|-----
A       | @    | [IP Address] | Automatic
```

**To add each A record:**

1. **Click "Add New Record"** button
2. **Select "A Record"** from the Type dropdown
3. **In the "Host" field, type: `@`** (just the @ symbol)
4. **In the "Value" field, enter one of these IP addresses:**
   - `34.143.72.2`
   - `34.143.73.2`
   - `34.143.74.2`
   - `34.143.75.2`
   - `34.143.76.2`
   - `34.143.77.2`
   - `34.143.78.2`
   - `34.143.79.2`
5. **Set TTL to "Automatic"**
6. **Click "Save"**

**Repeat this process 8 times** - once for each IP address.

### Step 5: Add CNAME Records

After adding all A records, add the CNAME records:

1. **Click "Add New Record"** again
2. **Select "CNAME Record"** from Type dropdown
3. **For API subdomain:**
   - Host: `api`
   - Value: `footybets-backend-818397187963.us-central1.run.app`
   - TTL: Automatic
4. **For www subdomain:**
   - Host: `www`
   - Value: `footybets-frontend-818397187963.us-central1.run.app`
   - TTL: Automatic

### Step 6: Final Result

Your DNS records should look like this:

```
Host Records
Type    | Host | Value                                                    | TTL
--------|------|----------------------------------------------------------|-----
A       | @    | 34.143.72.2                                              | Automatic
A       | @    | 34.143.73.2                                              | Automatic
A       | @    | 34.143.74.2                                              | Automatic
A       | @    | 34.143.75.2                                              | Automatic
A       | @    | 34.143.76.2                                              | Automatic
A       | @    | 34.143.77.2                                              | Automatic
A       | @    | 34.143.78.2                                              | Automatic
A       | @    | 34.143.79.2                                              | Automatic
CNAME   | api  | footybets-backend-818397187963.us-central1.run.app      | Automatic
CNAME   | www  | footybets-frontend-818397187963.us-central1.run.app     | Automatic
```

### Step 7: Save Everything

- Click **"Save All Changes"** button at the bottom
- Wait for the confirmation message

## 🚨 Important Notes

- **Don't include "https://"** in any values
- **Make sure Host is exactly "@"** (not "footybets.ai")
- **Add all 8 A records** - this provides load balancing
- **Wait 15-30 minutes** for DNS propagation

## 🔍 Testing

After saving, test with:
```bash
nslookup footybets.ai
nslookup api.footybets.ai
nslookup www.footybets.ai
```

## 🆘 If You Still Get Errors

If Namecheap still gives you errors with A records, use the **URL Redirect** method instead:

1. **Delete all A records**
2. **Add one URL Redirect record:**
   - Type: URL Redirect
   - Host: @
   - Value: `https://footybets-frontend-818397187963.us-central1.run.app`
   - TTL: Automatic

This will redirect `footybets.ai` directly to your frontend service. 