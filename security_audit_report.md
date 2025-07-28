# Google Cloud Security Audit Report
## FootyBets AI Project

### Executive Summary
This audit covers the security configuration of the FootyBets AI Google Cloud project. Overall, the configuration is generally secure, but there are several areas that need attention.

---

## 🔍 **Current Configuration Analysis**

### ✅ **Secure Configurations**

#### **1. Project Setup**
- **Project ID**: `footybets-ai`
- **Project Number**: `818397187963`
- **Owner**: `gmcintosh1985@gmail.com` (appropriate access level)

#### **2. IAM Configuration**
- **Owner Role**: Only you have owner access (good)
- **Service Accounts**: Properly configured for Cloud Run, Cloud Build, etc.
- **No Unnecessary Permissions**: No overly permissive roles found

#### **3. Cloud Run Services**
- **Backend**: `footybets-backend` - Running securely
- **Frontend**: `footybets-frontend` - Running securely
- **HTTPS**: Both services use HTTPS by default
- **Auto-scaling**: Properly configured (max 10 instances)

#### **4. Container Registry**
- **Images**: Properly stored in `gcr.io/footybets-ai`
- **Access**: Controlled through IAM

---

## ⚠️ **Security Issues Found**

### **1. Cloud SQL Database Security**

#### **Critical Issue: SSL Not Required**
```bash
# Current setting: requireSsl=False
# This means database connections are not encrypted!
```

**Risk**: Database connections are not encrypted, making them vulnerable to man-in-the-middle attacks.

**Recommendation**: Enable SSL requirement:
```bash
gcloud sql instances patch footybets-db --require-ssl
```

#### **Issue: Overly Permissive Network Access**
```bash
# Current setting: authorizedNetworks=0.0.0.0/0
# This allows access from ANY IP address!
```

**Risk**: Database is accessible from any IP address on the internet.

**Recommendation**: Restrict to specific IP ranges:
```bash
# Option 1: Restrict to Cloud Run IP ranges
gcloud sql instances patch footybets-db \
  --authorized-networks=0.0.0.0/0 \
  --require-ssl

# Option 2: Use Private Service Connect (recommended)
# This would require VPC configuration
```

### **2. Firewall Rules**

#### **Issue: Overly Permissive Rules**
```bash
# Current rules allow:
- SSH from anywhere (port 22)
- RDP from anywhere (port 3389)
- Internal traffic (all ports)
```

**Risk**: SSH and RDP are accessible from anywhere.

**Recommendation**: Restrict SSH access to your IP:
```bash
# Get your current IP
curl ifconfig.me

# Update SSH rule to your IP only
gcloud compute firewall-rules update default-allow-ssh \
  --source-ranges=YOUR_IP/32

# Consider removing RDP rule if not needed
gcloud compute firewall-rules delete default-allow-rdp
```

### **3. Environment Variables**

#### **Issue: Secrets in Environment Variables**
```bash
# Current environment variables contain:
- DATABASE_URL with plain text password
- SECRET_KEY in plain text
- API_SECRET_KEY in plain text
```

**Risk**: Secrets are visible in Cloud Run logs and configuration.

**Recommendation**: Use Secret Manager:
```bash
# Create secrets
echo -n "footybets_password" | gcloud secrets create db-password --data-file=-
echo -n "your-secret-key" | gcloud secrets create app-secret-key --data-file=-

# Update Cloud Run to use secrets
gcloud run services update footybets-backend \
  --region=us-central1 \
  --set-secrets=DATABASE_PASSWORD=db-password:latest,APP_SECRET_KEY=app-secret-key:latest
```

---

## 🔧 **Recommended Security Improvements**

### **1. Immediate Actions (High Priority)**

#### **Enable Database SSL**
```bash
gcloud sql instances patch footybets-db --require-ssl
```

#### **Restrict SSH Access**
```bash
# Get your IP
YOUR_IP=$(curl -s ifconfig.me)

# Update SSH firewall rule
gcloud compute firewall-rules update default-allow-ssh \
  --source-ranges=$YOUR_IP/32
```

#### **Remove Unnecessary Firewall Rules**
```bash
# Remove RDP if not needed
gcloud compute firewall-rules delete default-allow-rdp
```

### **2. Medium Priority Actions**

#### **Implement Secret Manager**
```bash
# Create secrets
echo -n "footybets_password" | gcloud secrets create db-password --data-file=-
echo -n "your-secret-key" | gcloud secrets create app-secret-key --data-file=-

# Grant Cloud Run access to secrets
gcloud secrets add-iam-policy-binding db-password \
  --member="serviceAccount:818397187963-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding app-secret-key \
  --member="serviceAccount:818397187963-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

#### **Enable Cloud Audit Logging**
```bash
# Enable audit logging for all services
gcloud services enable cloudaudit.googleapis.com
```

### **3. Advanced Security (Optional)**

#### **Implement VPC for Database**
```bash
# Create VPC
gcloud compute networks create footybets-vpc --subnet-mode=auto

# Create private subnet
gcloud compute networks subnets create private-subnet \
  --network=footybets-vpc \
  --region=us-central1 \
  --range=10.0.0.0/24

# Configure Cloud SQL for private access
gcloud sql instances patch footybets-db \
  --private-network-footybets-vpc
```

#### **Enable Cloud Armor**
```bash
# Enable Cloud Armor for DDoS protection
gcloud services enable compute.googleapis.com
gcloud compute security-policies create footybets-policy \
  --description="Security policy for FootyBets"
```

---

## 📊 **Security Score: 7/10**

### **Strengths:**
- ✅ Proper IAM configuration
- ✅ HTTPS enabled on Cloud Run
- ✅ Container images properly stored
- ✅ No unnecessary service accounts

### **Areas for Improvement:**
- ⚠️ Database SSL not required
- ⚠️ Database accessible from anywhere
- ⚠️ Secrets in plain text
- ⚠️ SSH accessible from anywhere

---

## 🚀 **Implementation Plan**

### **Phase 1: Critical Security (Immediate)**
1. Enable database SSL
2. Restrict SSH access
3. Remove RDP firewall rule

### **Phase 2: Secrets Management (This Week)**
1. Implement Secret Manager
2. Update Cloud Run to use secrets
3. Remove plain text secrets

### **Phase 3: Advanced Security (Next Week)**
1. Implement VPC for database
2. Enable Cloud Armor
3. Set up monitoring and alerting

---

## 📞 **Next Steps**

1. **Review this report** and prioritize the recommendations
2. **Implement Phase 1** immediately for critical security
3. **Schedule Phase 2** for this week
4. **Consider Phase 3** for advanced security features

Would you like me to implement any of these security improvements? 