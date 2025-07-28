# 🔒 Cloud SQL Security Implementation Guide

## 🚨 Current Security Issues

Your Cloud SQL instance `footybets-db` has the following security vulnerabilities:

1. **Exposed to broad public IP range** - Currently allows access from any IP (`0.0.0.0/0`)
2. **Auditing not enabled** - No database audit logs
3. **No password policy** - Weak password requirements
4. **No user password policy** - No user-specific password policies

## 🛡️ Security Implementation Plan

### Step 1: Restrict IP Access

#### Option A: Use Cloud Run Private Connection (Recommended)
```bash
# Enable private services access for Cloud Run
gcloud compute networks vpc-access connectors create footybets-connector \
    --region=us-central1 \
    --range=10.8.0.0/28 \
    --network=default \
    --min-instances=2 \
    --max-instances=10

# Update Cloud Run services to use private connection
gcloud run services update footybets-backend \
    --region=us-central1 \
    --vpc-connector=footybets-connector \
    --vpc-connector-egress=private-ranges-only

gcloud run services update footybets-frontend \
    --region=us-central1 \
    --vpc-connector=footybets-connector \
    --vpc-connector-egress=private-ranges-only
```

#### Option B: Restrict to Specific IP Ranges
```bash
# Remove broad access
gcloud sql instances patch footybets-db \
    --authorized-networks="" \
    --project=footybets-ai

# Add only necessary IP ranges
gcloud sql instances patch footybets-db \
    --authorized-networks="YOUR_OFFICE_IP/32,YOUR_HOME_IP/32" \
    --project=footybets-ai
```

### Step 2: Enable Database Auditing

```bash
# Enable audit logging
gcloud sql instances patch footybets-db \
    --enable-audit-logs \
    --project=footybets-ai

# Configure audit logging settings
gcloud sql instances patch footybets-db \
    --audit-logs-config="logType=ADMIN_READ,logType=DATA_READ,logType=DATA_WRITE" \
    --project=footybets-ai
```

### Step 3: Implement Password Policies

#### Create Password Policy Function
```sql
-- Connect to your database and run this SQL
CREATE OR REPLACE FUNCTION validate_password_strength(password TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    -- Check minimum length (8 characters)
    IF length(password) < 8 THEN
        RAISE EXCEPTION 'Password must be at least 8 characters long';
    END IF;
    
    -- Check for uppercase letter
    IF password !~ '[A-Z]' THEN
        RAISE EXCEPTION 'Password must contain at least one uppercase letter';
    END IF;
    
    -- Check for lowercase letter
    IF password !~ '[a-z]' THEN
        RAISE EXCEPTION 'Password must contain at least one lowercase letter';
    END IF;
    
    -- Check for number
    IF password !~ '[0-9]' THEN
        RAISE EXCEPTION 'Password must contain at least one number';
    END IF;
    
    -- Check for special character
    IF password !~ '[!@#$%^&*(),.?":{}|<>]' THEN
        RAISE EXCEPTION 'Password must contain at least one special character';
    END IF;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
```

#### Create Password Change Trigger
```sql
-- Create trigger to enforce password policy on user updates
CREATE OR REPLACE FUNCTION enforce_password_policy()
RETURNS TRIGGER AS $$
BEGIN
    -- Only check if password is being changed
    IF NEW.hashed_password != OLD.hashed_password THEN
        -- Note: We can't validate the plain text password here since it's hashed
        -- This validation should be done in the application layer
        -- This trigger is mainly for audit purposes
        INSERT INTO security_logs (user_id, action, details, ip_address)
        VALUES (NEW.id, 'password_change', 'Password updated', 'system');
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER password_policy_trigger
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION enforce_password_policy();
```

### Step 4: Update Application Security

#### Update Database Configuration
```python
# backend/app/core/database.py - Add SSL configuration
def create_database_engine():
    """Create database engine with appropriate configuration"""
    
    # Base configuration
    engine_kwargs = {
        "echo": settings.debug,
        "pool_pre_ping": True,
    }
    
    # PostgreSQL/Production settings with SSL
    if "postgresql" in settings.database_url:
        engine_kwargs.update({
            "poolclass": QueuePool,
            "pool_size": 20,
            "max_overflow": 30,
            "pool_timeout": 30,
            "pool_recycle": 3600,
            "connect_args": {
                "sslmode": "require",  # Force SSL connection
                "application_name": "footybets-backend"
            }
        })
    
    return create_engine(settings.database_url, **engine_kwargs)
```

#### Update Environment Variables
```bash
# Update your deployment scripts to use private connection
DATABASE_URL=postgresql://footybets_user:footybets_password@/footybets-ai:us-central1:footybets-db/footybets?sslmode=require
```

### Step 5: Implement Application-Level Password Validation

```python
# backend/app/core/security.py - Add password validation
import re

def validate_password_strength(password: str) -> bool:
    """Validate password meets security requirements"""
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    
    if not re.search(r'[A-Z]', password):
        raise ValueError("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        raise ValueError("Password must contain at least one lowercase letter")
    
    if not re.search(r'[0-9]', password):
        raise ValueError("Password must contain at least one number")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError("Password must contain at least one special character")
    
    return True

def create_user_with_secure_password(db: Session, user_data: dict) -> User:
    """Create user with password validation"""
    # Validate password strength
    validate_password_strength(user_data['password'])
    
    # Hash password
    hashed_password = hash_password(user_data['password'])
    
    # Create user
    user = User(
        email=user_data['email'],
        username=user_data['username'],
        hashed_password=hashed_password,
        # ... other fields
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user
```

### Step 6: Enable Cloud SQL Proxy for Development

```bash
# Install Cloud SQL Proxy
curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64
chmod +x cloud_sql_proxy

# Start proxy for development
./cloud_sql_proxy -instances=footybets-ai:us-central1:footybets-db=tcp:5432
```

### Step 7: Update Deployment Scripts

```bash
# deploy-update.sh - Update to use private connection
gcloud run services update footybets-backend \
    --region=us-central1 \
    --set-env-vars="DATABASE_URL=postgresql://footybets_user:footybets_password@/footybets-ai:us-central1:footybets-db/footybets?sslmode=require" \
    --vpc-connector=footybets-connector \
    --vpc-connector-egress=private-ranges-only
```

### Step 8: Monitor and Audit

#### Create Security Monitoring Dashboard
```python
# backend/app/api/routes/admin.py - Add security monitoring
@router.get("/security/audit-logs")
async def get_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
    limit: int = 100,
    offset: int = 0
):
    """Get security audit logs"""
    logs = db.query(SecurityLog)\
        .order_by(SecurityLog.created_at.desc())\
        .offset(offset)\
        .limit(limit)\
        .all()
    
    return {
        "logs": logs,
        "total": db.query(SecurityLog).count()
    }

@router.get("/security/failed-logins")
async def get_failed_logins(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
    days: int = 7
):
    """Get failed login attempts"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    failed_logins = db.query(SecurityLog)\
        .filter(SecurityLog.action == "failed_login")\
        .filter(SecurityLog.created_at >= cutoff_date)\
        .all()
    
    return {
        "failed_logins": failed_logins,
        "total_attempts": len(failed_logins),
        "period_days": days
    }
```

## 🔍 Verification Steps

### 1. Test Private Connection
```bash
# Test connection from Cloud Run
gcloud run services call footybets-backend \
    --region=us-central1 \
    --data='{"test": "database_connection"}'
```

### 2. Verify SSL Connection
```bash
# Check SSL connection in logs
gcloud logging read "resource.type=cloudsql_database" \
    --project=footybets-ai \
    --limit=10
```

### 3. Test Password Policy
```bash
# Try to register with weak password
curl -X POST "https://footybets-backend-818397187963.us-central1.run.app/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "weak"
  }'
# Should return password validation error
```

### 4. Check Audit Logs
```bash
# View audit logs
gcloud logging read "resource.type=cloudsql_database AND logName:audit" \
    --project=footybets-ai \
    --limit=10
```

## 🚨 Emergency Rollback

If something goes wrong, you can quickly rollback:

```bash
# Re-enable public access temporarily
gcloud sql instances patch footybets-db \
    --authorized-networks="0.0.0.0/0" \
    --project=footybets-ai

# Restart services
gcloud run services update footybets-backend --region=us-central1
gcloud run services update footybets-frontend --region=us-central1
```

## 📊 Security Metrics

After implementation, monitor these metrics:

1. **Connection Security**: All connections should use SSL
2. **Access Control**: Only authorized IPs should connect
3. **Password Strength**: All new passwords should meet requirements
4. **Audit Coverage**: All database operations should be logged
5. **Failed Login Attempts**: Monitor for suspicious activity

## 🔐 Additional Security Recommendations

1. **Enable Cloud Armor**: Protect against DDoS attacks
2. **Set up Alerting**: Get notified of security events
3. **Regular Backups**: Automated encrypted backups
4. **Key Rotation**: Regular API key rotation
5. **Vulnerability Scanning**: Regular security scans

## 📞 Support

If you encounter issues during implementation:

1. Check Cloud SQL logs: `gcloud logging read "resource.type=cloudsql_database"`
2. Check Cloud Run logs: `gcloud logging read "resource.type=cloud_run_revision"`
3. Test connectivity: Use Cloud SQL Proxy for troubleshooting
4. Review security logs: Check the admin dashboard

This implementation will address all the security issues identified in your Cloud SQL instance while maintaining application functionality. 