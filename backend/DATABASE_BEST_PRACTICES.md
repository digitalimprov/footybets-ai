# 🗄️ Database Best Practices Guide

This document outlines the database best practices implemented in FootyBets.ai and recommendations for production deployment.

## ✅ **Current Implementation Status**

### **Security & Authentication**
- ✅ **Password Hashing**: bcrypt with salt
- ✅ **JWT Tokens**: Secure token management
- ✅ **Role-Based Access Control**: Granular permissions
- ✅ **Session Management**: Secure session handling
- ✅ **Audit Logging**: Comprehensive security logs
- ✅ **Input Validation**: Pydantic models for validation

### **Data Modeling**
- ✅ **Proper Relationships**: Foreign keys and back-references
- ✅ **Indexing**: Strategic indexes on frequently queried fields
- ✅ **Audit Fields**: `created_at`, `updated_at` timestamps
- ✅ **Soft Deletes**: Account for data retention
- ✅ **JSON Fields**: Flexible data storage where appropriate

### **Connection Management**
- ✅ **Connection Pooling**: Configured for production
- ✅ **Session Management**: Proper session lifecycle
- ✅ **Error Handling**: Comprehensive error handling
- ✅ **Connection Testing**: Health check functionality

## 🚀 **Recent Improvements**

### **1. Enhanced Database Configuration**
```python
# Production-ready connection pooling
engine = create_engine(
    settings.database_url,
    pool_size=20,           # Maintain 20 connections
    max_overflow=30,        # Allow 30 additional connections
    pool_timeout=30,        # 30-second timeout
    pool_recycle=3600,      # Recycle connections every hour
    pool_pre_ping=True      # Verify connections before use
)
```

### **2. Database Migrations (Alembic)**
```bash
# Initialize migrations
alembic init alembic

# Create new migration
alembic revision --autogenerate -m "Add new feature"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### **3. Automated Backups**
```bash
# Create backup
python database_backup.py

# List backups
python -c "from database_backup import DatabaseBackup; db = DatabaseBackup(); print(db.list_backups())"
```

## 📊 **Performance Optimizations**

### **Indexing Strategy**
```sql
-- Frequently queried fields
CREATE INDEX idx_games_season_round ON games(season, round_number);
CREATE INDEX idx_predictions_game_date ON predictions(prediction_date);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
```

### **Query Optimization**
```python
# Use select() for better performance
from sqlalchemy.orm import selectinload

# Eager loading to avoid N+1 queries
users = db.query(User).options(
    selectinload(User.user_tips),
    selectinload(User.sessions)
).all()
```

### **Connection Pooling**
```python
# Production settings
pool_size = 20          # Base pool size
max_overflow = 30       # Additional connections when busy
pool_timeout = 30       # Timeout for getting connection
pool_recycle = 3600     # Recycle connections every hour
```

## 🔒 **Security Best Practices**

### **1. Password Security**
```python
# bcrypt hashing with salt
def set_password(self, password: str):
    self.hashed_password = bcrypt.hashpw(
        password.encode('utf-8'), 
        bcrypt.gensalt()
    ).decode('utf-8')

def verify_password(self, password: str) -> bool:
    return bcrypt.checkpw(
        password.encode('utf-8'), 
        self.hashed_password.encode('utf-8')
    )
```

### **2. SQL Injection Prevention**
```python
# Use parameterized queries (SQLAlchemy handles this)
user = db.query(User).filter(User.email == email).first()

# Never use string formatting for queries
# ❌ BAD: f"SELECT * FROM users WHERE email = '{email}'"
# ✅ GOOD: db.query(User).filter(User.email == email)
```

### **3. Input Validation**
```python
# Pydantic models for validation
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)
```

## 📈 **Monitoring & Maintenance**

### **1. Database Health Checks**
```python
def test_database_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False
```

### **2. Performance Monitoring**
```python
# Enable SQL query logging in development
engine = create_engine(
    settings.database_url,
    echo=settings.debug  # Log all SQL queries
)
```

### **3. Backup Strategy**
```python
# Automated daily backups
# - Full database backup
# - Incremental backups for large datasets
# - Point-in-time recovery capability
# - Backup verification
```

## 🚨 **Production Recommendations**

### **1. Database Choice**
- **Development**: SQLite (current)
- **Production**: PostgreSQL (recommended)
- **Scaling**: Consider read replicas for high traffic

### **2. Environment Variables**
```env
# Production database
DATABASE_URL=postgresql://user:password@host:5432/footybets

# Connection pooling
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
```

### **3. Backup Schedule**
```bash
# Daily automated backups
0 2 * * * /path/to/python /app/database_backup.py

# Weekly full backups
0 3 * * 0 /path/to/python /app/database_backup.py --full

# Monthly backup verification
0 4 1 * * /path/to/python /app/verify_backup.py
```

### **4. Monitoring Setup**
```python
# Database metrics
- Connection pool usage
- Query performance
- Lock contention
- Disk space usage
- Backup success/failure
```

## 🔧 **Migration Strategy**

### **From SQLite to PostgreSQL**
1. **Create migration script**
2. **Test data migration**
3. **Update connection strings**
4. **Verify data integrity**
5. **Update backup procedures**

### **Schema Evolution**
```bash
# Create migration for new feature
alembic revision --autogenerate -m "Add user preferences"

# Review generated migration
# Edit if needed

# Apply to development
alembic upgrade head

# Test thoroughly

# Apply to production
alembic upgrade head
```

## 📋 **Checklist for Production**

- [ ] **Database Migrations**: Alembic setup and tested
- [ ] **Connection Pooling**: Configured for expected load
- [ ] **Backup Strategy**: Automated and tested
- [ ] **Monitoring**: Health checks and metrics
- [ ] **Security**: All security features enabled
- [ ] **Performance**: Indexes and query optimization
- [ ] **Documentation**: Schema and procedures documented
- [ ] **Disaster Recovery**: Backup restoration tested

## 🎯 **Next Steps**

1. **Implement PostgreSQL migration**
2. **Set up automated monitoring**
3. **Create disaster recovery plan**
4. **Performance testing under load**
5. **Security audit and penetration testing**

---

*This guide should be updated as the application evolves and new best practices emerge.* 