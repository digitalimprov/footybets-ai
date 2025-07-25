# 👥 Roles and Permissions Guide

FootyBets.ai implements a comprehensive role-based access control (RBAC) system with four distinct user roles, each with specific permissions and capabilities.

## 🎯 Available Roles

### 1. **User (Free Tier)**
**Default role for all registered users**

**Permissions:**
- ✅ Read predictions
- ✅ Read analytics
- ✅ Read games
- ✅ Read own profile
- ✅ Write own profile

**Features:**
- Access to basic AI predictions
- View upcoming games
- Access to analytics dashboard
- Manage personal profile

### 2. **Subscriber (Paid Tier)**
**Enhanced access for paying users**

**Permissions:**
- ✅ All User permissions
- ✅ Write user tips
- ✅ Read user tips

**Features:**
- All free tier features
- Submit and view user tips
- Priority support

**Subscription Tiers:**
- **Basic**: $9.99/month
- **Premium**: $19.99/month  
- **Pro**: $29.99/month

### 3. **Moderator**
**Content moderation and user management**

**Permissions:**
- ✅ All Subscriber permissions
- ✅ Read users
- ✅ Write users
- ✅ Moderate user tips
- ✅ View security logs

**Features:**
- All subscriber features
- User management capabilities
- Content moderation tools
- Security log access
- Community management

### 4. **Admin**
**Full system access and control**

**Permissions:**
- ✅ All permissions (full access)
- ✅ Manage scraping
- ✅ Manage AI
- ✅ Manage roles
- ✅ Export data
- ✅ Manage subscriptions
- ✅ System administration

**Features:**
- Complete system control
- User role management
- System configuration
- Data management
- Security administration
- Analytics and reporting

## 🔐 Permission System

### Core Permissions

| Permission | Description | Roles |
|------------|-------------|-------|
| `read_predictions` | View AI predictions | All |
| `write_predictions` | Create/modify predictions | Admin |
| `read_analytics` | View analytics data | All |
| `write_analytics` | Modify analytics | Admin |
| `read_games` | View game data | All |
| `write_games` | Modify game data | Admin |
| `read_users` | View user information | Moderator+ |
| `write_users` | Modify user information | Moderator+ |
| `read_system` | View system information | Admin |
| `write_system` | Modify system settings | Admin |
| `manage_scraping` | Control data scraping | Admin |
| `manage_ai` | Control AI predictions | Admin |
| `view_security_logs` | Access security logs | Moderator+ |
| `manage_roles` | Assign user roles | Admin |
| `export_data` | Export system data | Admin |
| `manage_subscriptions` | Manage user subscriptions | Admin |
| `write_user_tips` | Submit user tips | Subscriber+ |
| `read_user_tips` | View user tips | Subscriber+ |
| `moderate_user_tips` | Moderate user content | Moderator+ |
| `read_own_profile` | View own profile | All |
| `write_own_profile` | Edit own profile | All |

## 🚀 Role Management

### Creating Your First Admin

After setting up the platform, create your first admin user:

```bash
# 1. Register a regular user
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@footybets.ai",
    "username": "admin",
    "password": "SecurePass123!",
    "first_name": "Admin",
    "last_name": "User"
  }'

# 2. Login to get access token
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@footybets.ai",
    "password": "SecurePass123!"
  }'

# 3. Promote to admin (using the access token)
curl -X POST "http://localhost:8000/api/admin/users/1/promote-admin" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Managing User Roles

#### Promote User to Admin
```bash
curl -X POST "http://localhost:8000/api/admin/users/{user_id}/promote-admin" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Demote Admin to User
```bash
curl -X POST "http://localhost:8000/api/admin/users/{user_id}/demote-admin" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Upgrade User Subscription
```bash
curl -X POST "http://localhost:8000/api/admin/users/{user_id}/upgrade-subscription" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tier": "premium",
    "duration_days": 30
  }'
```

#### Downgrade User Subscription
```bash
curl -X POST "http://localhost:8000/api/admin/users/{user_id}/downgrade-subscription" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📊 Admin Dashboard Features

### User Management
- **View all users** with filtering and search
- **Edit user profiles** and settings
- **Manage user roles** and permissions
- **Handle subscriptions** and billing
- **Unlock locked accounts**
- **View user sessions** and activity

### System Administration
- **System statistics** and metrics
- **Security logs** and audit trails
- **Role management** and permissions
- **Data export** and backup
- **System configuration**

### Content Moderation
- **User tips moderation**
- **Content filtering**
- **Community management**
- **Report handling**

## 🔒 Security Features by Role

### User (Free)
- Basic account security
- Password protection
- Session management

### Subscriber
- Enhanced security features
- API key access
- Secure data export

### Moderator
- User management tools
- Security log access
- Content moderation tools

### Admin
- Full security control
- System administration
- Complete audit access
- Security configuration

## 💰 Subscription Management

### Subscription Tiers

| Tier | Price | Features | Permissions |
|------|-------|----------|-------------|
| **Free** | $0 | Basic predictions, Games, Analytics | User role |
| **Basic** | $9.99/month | + User tips | Subscriber role |
| **Premium** | $19.99/month | + Priority support | Subscriber role |
| **Pro** | $29.99/month | + API access | Subscriber role |
| **Admin** | N/A | Full system access | Admin role |

### Subscription Features

#### Basic Tier
- AI predictions
- Analytics access
- User tips
- Email support

#### Premium Tier
- All Basic features
- Priority support
- Enhanced features

#### Pro Tier
- All Premium features
- API access
- Custom integrations
- Dedicated support

## 🛡️ Security Considerations

### Role-Based Security
- **Principle of Least Privilege**: Users only get necessary permissions
- **Role Separation**: Clear boundaries between roles
- **Audit Logging**: All role changes are logged
- **Permission Validation**: Server-side permission checks

### Admin Security
- **Admin Protection**: Admins cannot accidentally demote themselves
- **Session Management**: Admin sessions are closely monitored
- **Security Logs**: All admin actions are logged
- **Multi-factor Authentication**: Ready for implementation

### Data Protection
- **Role-Based Data Access**: Users only see data they're authorized to access
- **Encrypted Storage**: Sensitive data is encrypted
- **Audit Trails**: Complete audit trails for all data access
- **Data Export Controls**: Controlled data export capabilities

## 🔧 Implementation Details

### Database Schema
```sql
-- User roles are stored as JSON array
roles: ["user", "subscriber", "admin"]

-- Permissions are automatically calculated based on roles
permissions: ["read_predictions", "read_games", "read_analytics"]

-- Subscription information
subscription_tier: "premium"
subscription_expires: "2024-12-31T23:59:59Z"
```

### API Endpoints
- `/api/admin/users` - User management
- `/api/admin/roles` - Role management
- `/api/admin/subscriptions` - Subscription management
- `/api/admin/security-logs` - Security monitoring
- `/api/admin/system-stats` - System statistics

### Frontend Integration
- Role-based UI rendering
- Permission-based feature access
- Subscription tier display
- Admin dashboard components

## 📈 Usage Examples

### Check User Permissions
```python
# In your code
if current_user.has_permission("read_analytics"):
    # Show analytics
    pass

if current_user.has_role("admin"):
    # Show admin features
    pass
```

### Role-Based API Access
```python
# Protect endpoints with role requirements
@router.get("/admin/users")
async def get_users(current_user: User = Depends(require_permission("read_users"))):
    # Only users with read_users permission can access
    pass
```

### Subscription Checks
```python
# Check subscription status
if current_user.is_subscriber:
    # Show subscriber features
    pass

if current_user.subscription_tier == "premium":
    # Show premium features
    pass
```

## 🎯 Best Practices

### Role Assignment
1. **Start with minimal permissions**
2. **Grant additional permissions as needed**
3. **Regularly review user roles**
4. **Document role changes**

### Security
1. **Monitor admin actions**
2. **Regular security audits**
3. **Implement least privilege**
4. **Log all role changes**

### User Experience
1. **Clear role descriptions**
2. **Intuitive permission system**
3. **Helpful error messages**
4. **Role-based UI**

This role-based system ensures that your FootyBets.ai platform is secure, scalable, and user-friendly while providing the flexibility to grow your user base with different subscription tiers and access levels. 