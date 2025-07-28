# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Backend (FastAPI Python)
- **Start development server**: `cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8080`
- **Install dependencies**: `cd backend && pip install -r requirements.txt`
- **Database migrations**: `cd backend && alembic upgrade head`
- **Create migration**: `cd backend && alembic revision --autogenerate -m "description"`

### Frontend (React)
- **Start development server**: `cd frontend && npm start`
- **Install dependencies**: `cd frontend && npm install`
- **Build for production**: `cd frontend && npm run build`
- **Run tests**: `cd frontend && npm test`

### Deployment
- **Quick deployment**: `./deploy-update.sh` (requires Google Cloud CLI setup)
- **Full deployment**: Uses `cloudbuild.yaml` for Google Cloud Build
- **Production URLs**: 
  - Frontend: https://footybets-frontend-818397187963.us-central1.run.app
  - Backend: https://footybets-backend-818397187963.us-central1.run.app

## Architecture Overview

### System Design
This is an AI-powered AFL betting predictions platform with three main components:

1. **Backend** (`/backend`): FastAPI application with comprehensive security middleware
2. **Frontend** (`/frontend`): React.js single-page application
3. **Mobile** (`/mobile`): React Native mobile app

### Backend Architecture (`/backend/app`)
- **`main.py`**: FastAPI app initialization with security middleware, CORS, rate limiting
- **`core/`**: Core application configuration, database, and security
  - `config.py`: Environment-based settings management
  - `database.py`: SQLAlchemy engine with connection pooling and SSL
  - `security.py`: JWT authentication, rate limiting, security logging
- **`models/`**: SQLAlchemy database models (User, Game, Prediction, etc.)
- **`api/routes/`**: API endpoints organized by feature (auth, games, predictions, admin)
- **`services/`**: Business logic services (content_service, email_service)
- **`ai/`**: AI prediction engine using Google Gemini API
- **`scrapers/`**: AFL data scraping utilities

### Database Schema
- **PostgreSQL** in production with SSL enforcement
- **SQLite** for local development
- Key tables: `users`, `games`, `predictions`, `teams`, `players`, `analytics`
- Role-based permissions system (admin, subscriber, free_user)

### Security Features
- JWT authentication with role-based access control
- Rate limiting with higher limits for admin users
- Comprehensive security logging and monitoring
- Request validation and SQL injection protection
- CORS and trusted host middleware for production

### AI Integration
- **Google Gemini API** for predictions and content generation
- **Prediction engine** at `app/ai/predictor.py`
- **Brownlow Medal predictions** with historical analysis
- **Content generation** with witty, betting-focused tone

### Deployment Strategy
- **Google Cloud Run** for both frontend and backend
- **Docker containerization** with multi-stage builds
- **Cloud Build** for automated CI/CD
- **Cloud SQL PostgreSQL** for production database
- **Cloud Storage** for static Brownlow content

## Key Development Patterns

### Authentication Flow
- JWT tokens with role-based permissions
- Admin users have elevated rate limits and additional endpoints
- Security events logged for monitoring

### Data Flow
1. AFL data scraped and stored in database
2. AI engine generates predictions using historical data
3. Frontend displays predictions with real-time updates
4. Content service generates SEO-optimized pages

### Error Handling
- Comprehensive exception handlers in `main.py`
- Security event logging for suspicious requests
- Input validation with detailed error responses

## Environment Setup
- Backend requires: `DATABASE_URL`, `GEMINI_API_KEY`, `API_SECRET_KEY`
- Frontend requires: `REACT_APP_API_URL`
- Production uses Google Cloud Run environment variables