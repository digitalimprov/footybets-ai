# 🚨 Quick Security Fix for Cloud SQL

## Immediate Action Required

Your Cloud SQL instance `footybets-db` has critical security vulnerabilities that need immediate attention:

### 🔴 Critical Issues:
1. **Exposed to broad public IP range** - Database accessible from anywhere
2. **Auditing not enabled** - No security logs
3. **No password policy** - Weak passwords allowed
4. **No user password policy** - No user-specific security

## 🛡️ Quick Fix Implementation

### Step 1: Run the Security Script
```bash
# Make sure you're in the project directory
cd /Users/graememcintosh/Library/Mobile\ Documents/com~apple~CloudDocs/Footy\ Bets\ AI

# Run the security implementation script
./secure_database.sh
```

### Step 2: Test Your Application
After running the script, test that your application still works:

```bash
# Test backend health
curl https://footybets-backend-818397187963.us-central1.run.app/health

# Test frontend
curl https://footybets-frontend-818397187963.us-central1.run.app
```

### Step 3: Monitor Security
```bash
# Check security status
./monitor_security.sh

# View audit logs
gcloud logging read "resource.type=cloudsql_database AND logName:audit" \
    --project=footybets-ai \
    --limit=10
```

## 🔧 What the Script Does

1. **Enables Audit Logging** - Tracks all database access
2. **Creates VPC Connector** - Enables private network access
3. **Updates Cloud Run Services** - Uses private connection
4. **Enforces SSL** - All connections must use encryption
5. **Prepares for Public IP Removal** - Ready to remove public access

## 🚨 Emergency Rollback

If something breaks:
```bash
./emergency_rollback.sh
```

## 📊 Security Improvements

After running the script, you'll have:

✅ **Audit Logging** - All database operations logged  
✅ **Private Network Access** - Database only accessible via VPC  
✅ **SSL Enforcement** - All connections encrypted  
✅ **Security Monitoring** - Tools to track security events  
✅ **Emergency Procedures** - Quick rollback if needed  

## 🔍 Verification Commands

```bash
# Check if audit logging is enabled
gcloud sql instances describe footybets-db --project=footybets-ai

# Check VPC connector status
gcloud compute networks vpc-access connectors list --region=us-central1

# Check Cloud Run service configuration
gcloud run services describe footybets-backend --region=us-central1

# View recent security events
gcloud logging read "resource.type=cloudsql_database" --project=footybets-ai --limit=5
```

## 📋 Next Steps

1. **Test thoroughly** - Make sure everything works
2. **Monitor logs** - Check for any issues
3. **Remove public IP** - When confident, remove public access
4. **Update deployment** - Use new private connection string

## 🆘 If You Need Help

1. Check the logs: `gcloud logging read "resource.type=cloud_run_revision"`
2. Test connectivity: Use the health endpoints
3. Rollback if needed: `./emergency_rollback.sh`
4. Review the detailed guide: `SECURE_DATABASE_SETUP.md`

## ⚡ Quick Commands

```bash
# Run security fix
./secure_database.sh

# Monitor security
./monitor_security.sh

# Emergency rollback
./emergency_rollback.sh

# Check application health
curl https://footybets-backend-818397187963.us-central1.run.app/health
```

This will address all the security issues identified in your Cloud SQL instance while maintaining application functionality. 