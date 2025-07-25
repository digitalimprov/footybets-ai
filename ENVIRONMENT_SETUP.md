# 🚀 Getting Started with FootyBets.ai

This guide will walk you through setting up your FootyBets.ai platform with all security features enabled.

## 📋 Prerequisites

Before you begin, make sure you have:

- **Docker and Docker Compose** installed
- **Python 3.11+** (for local development)
- **Node.js 18+** (for frontend development)
- **Git** for version control
- **A Google Gemini API key** (free tier available)

## 🔧 Step 1: Environment Setup

### 1.1 Clone the Repository
```bash
git clone <your-repository-url>
cd footybets-ai
```

### 1.2 Create Environment File
```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your configuration
nano .env  # or use your preferred editor
```

### 1.3 Configure Environment Variables

Fill in your `.env` file with the following essential values:

```bash
# =============================================================================
# SECURITY SETTINGS (GENERATE THESE!)
# =============================================================================
# Generate secure keys using Python:
# python -c "import secrets; print(secrets.token_urlsafe(32))"

SECRET_KEY=your-generated-secret-key-here
ENCRYPTION_KEY=your-generated-encryption-key-here

# =============================================================================
# GOOGLE GEMINI AI API
# =============================================================================
# Get your free API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# =============================================================================
# EMAIL CONFIGURATION (OPTIONAL FOR STARTUP)
# =============================================================================
# For Gmail, create an App Password: https://support.google.com/accounts/answer/185833
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@footybets.ai
FROM_NAME=FootyBets.ai

# =============================================================================
# DATABASE (Docker will handle this)
# =============================================================================
DATABASE_URL=postgresql://footybets_user:footybets_password@postgres:5432/footybets

# =============================================================================
# FRONTEND URL
# =============================================================================
FRONTEND_URL=http://localhost:3000
```

## 🐳 Step 2: Start with Docker (Recommended)

### 2.1 Start All Services
```bash
# Start the entire platform
docker-compose up -d

# Check if all services are running
docker-compose ps
```

### 2.2 Verify Services
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: PostgreSQL on port 5432

## 🔍 Step 3: Initial Setup

### 3.1 Check API Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": 1234567890.123,
  "environment": "development"
}
```

### 3.2 Check Security Info
```bash
curl http://localhost:8000/security
```

This will show all enabled security features.

## 📊 Step 4: Load Initial Data

### 4.1 Scrape Historical AFL Data
1. Go to http://localhost:3000/scraping
2. Click "Scrape Historical Data"
3. This will load 5 years of AFL data (takes 5-10 minutes)

### 4.2 Generate AI Predictions
1. Go to http://localhost:3000/predictions
2. Click "Generate Predictions"
3. This will create AI predictions for upcoming games

## 👤 Step 5: Create Your First User

### 5.1 Register via API
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@footybets.ai",
    "username": "admin",
    "password": "SecurePass123!",
    "first_name": "Admin",
    "last_name": "User"
  }'
```

### 5.2 Login to Get Tokens
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@footybets.ai",
    "password": "SecurePass123!"
  }'
```

### 5.3 Use the Frontend
1. Go to http://localhost:3000
2. Click "Register" or "Login"
3. Complete the registration process
4. Verify your email (check console logs if email not configured)

## 🔒 Step 6: Security Verification

### 6.1 Test Security Features
```bash
# Test rate limiting
for i in {1..11}; do
  curl http://localhost:8000/api/games
  echo "Request $i"
done

# Test authentication
curl http://localhost:8000/api/auth/me
# Should return 401 Unauthorized
```

### 6.2 Check Security Headers
```bash
curl -I http://localhost:8000
```

You should see security headers like:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`

## 📱 Step 7: Mobile App Setup (Optional)

### 7.1 Install Dependencies
```bash
cd mobile
npm install
```

### 7.2 Configure Mobile App
```bash
# Copy mobile environment file
cp .env.example .env

# Edit mobile environment
nano .env
```

### 7.3 Start Mobile Development
```bash
# Start Expo development server
npm start

# Run on iOS simulator
npm run ios

# Run on Android emulator
npm run android
```

## 🧪 Step 8: Testing Your Setup

### 8.1 Test Core Features
1. **Dashboard**: View system overview
2. **Predictions**: Check AI predictions
3. **Analytics**: View performance metrics
4. **Games**: Browse AFL games
5. **Scraping**: Monitor data collection

### 8.2 Test Security Features
1. **Registration**: Try weak passwords (should be rejected)
2. **Login**: Try wrong credentials (should lock account)
3. **Rate Limiting**: Make many requests quickly
4. **Session Management**: Test token expiration

## 🚨 Troubleshooting

### Common Issues

#### 1. Database Connection Failed
```bash
# Check if PostgreSQL is running
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

#### 2. API Not Responding
```bash
# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

#### 3. Frontend Not Loading
```bash
# Check frontend logs
docker-compose logs frontend

# Restart frontend
docker-compose restart frontend
```

#### 4. Email Not Working
- Check SMTP settings in `.env`
- For Gmail, use App Password, not regular password
- Check console logs for email errors

#### 5. Gemini API Errors
- Verify your API key is correct
- Check API quota limits
- Ensure internet connection

### Debug Mode
```bash
# Enable debug mode
export DEBUG=true

# View detailed logs
docker-compose logs -f
```

## 🔄 Development Workflow

### Daily Development
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

### Code Changes
- Backend changes auto-reload
- Frontend changes auto-reload
- Database changes require migration

### Database Migrations
```bash
# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec backend alembic upgrade head
```

## 📈 Next Steps

### 1. Production Deployment
- Set up production environment
- Configure SSL certificates
- Set up monitoring and logging
- Configure backup procedures

### 2. Feature Development
- Implement user tips feature
- Add more analytics
- Enhance AI predictions
- Add mobile-specific features

### 3. Security Hardening
- Set up intrusion detection
- Configure firewall rules
- Implement backup encryption
- Set up security monitoring

## 📞 Support

If you encounter issues:

1. **Check the logs**: `docker-compose logs [service-name]`
2. **Verify configuration**: Check your `.env` file
3. **Test connectivity**: Ensure all services can communicate
4. **Review documentation**: Check README.md and SECURITY_GUIDE.md

## 🎉 Congratulations!

You now have a fully functional, secure FootyBets.ai platform running locally! 

**What you can do next:**
- Explore the API documentation at http://localhost:8000/docs
- Test the frontend at http://localhost:3000
- Start developing new features
- Prepare for production deployment

**Remember:**
- Keep your `.env` file secure and never commit it to version control
- Regularly update dependencies for security patches
- Monitor logs for any security events
- Test all features thoroughly before production deployment

Happy coding! 🚀 