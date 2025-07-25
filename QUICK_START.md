# ⚡ Quick Start Guide

Get FootyBets.ai running in 5 minutes!

## 🚀 Super Quick Setup

### 1. Generate Security Keys
```bash
# Run this to generate secure keys
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32)); print('ENCRYPTION_KEY=' + secrets.token_urlsafe(32))"
```

### 2. Create .env File
```bash
# Create environment file
cat > .env << 'EOF'
# Security (replace with your generated keys)
SECRET_KEY=your-generated-secret-key-here
ENCRYPTION_KEY=your-generated-encryption-key-here

# Google Gemini API (get free key from https://makersuite.google.com/app/apikey)
GEMINI_API_KEY=your_gemini_api_key_here

# Database (Docker handles this)
DATABASE_URL=postgresql://footybets_user:footybets_password@postgres:5432/footybets

# Frontend
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
DEBUG=true
EOF
```

### 3. Start Everything
```bash
# Start all services
docker-compose up -d

# Wait 30 seconds for services to start
sleep 30

# Check if everything is running
docker-compose ps
```

### 4. Test Your Setup
```bash
# Test API health
curl http://localhost:8000/health

# Test frontend (should show React app)
curl http://localhost:3000
```

### 5. Access Your Platform
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🎯 What's Running

✅ **Backend API** - FastAPI with security  
✅ **Frontend** - React with Tailwind CSS  
✅ **Database** - PostgreSQL with encryption  
✅ **Security** - JWT auth, rate limiting, encryption  
✅ **AI Integration** - Google Gemini ready  

## 🔧 Next Steps

1. **Get Gemini API Key**: https://makersuite.google.com/app/apikey
2. **Add it to .env**: `GEMINI_API_KEY=your_key_here`
3. **Restart services**: `docker-compose restart backend`
4. **Test AI**: Go to http://localhost:3000/predictions

## 🚨 If Something Goes Wrong

```bash
# Check logs
docker-compose logs

# Restart everything
docker-compose down
docker-compose up -d

# Still having issues? Check the full ENVIRONMENT_SETUP.md
```

## 🎉 You're Ready!

Your secure FootyBets.ai platform is now running! 

**Quick Test:**
- Visit http://localhost:3000
- Try registering a user
- Check out the API docs at http://localhost:8000/docs

**Need Help?** Check `ENVIRONMENT_SETUP.md` for detailed instructions. 