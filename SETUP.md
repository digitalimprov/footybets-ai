# FootyBets.ai Setup Guide

This guide will help you set up and run the FootyBets.ai application locally.

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)
- Google Gemini API key

## Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd footybets-ai
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Manual Setup (Development)

### Backend Setup

1. **Create virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp ../env.example .env
   # Edit .env with your configuration
   ```

4. **Set up database**
   ```bash
   # Install PostgreSQL locally or use Docker
   docker run -d --name footybets-postgres \
     -e POSTGRES_DB=footybets \
     -e POSTGRES_USER=footybets_user \
     -e POSTGRES_PASSWORD=footybets_password \
     -p 5432:5432 \
     postgres:15
   ```

5. **Run database migrations**
   ```bash
   # Create tables (you'll need to implement Alembic migrations)
   python -c "from app.core.database import engine; from app.models import *; Base.metadata.create_all(bind=engine)"
   ```

6. **Start the backend**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Set up environment variables**
   ```bash
   # Create .env file
   echo "REACT_APP_API_URL=http://localhost:8000" > .env
   ```

3. **Start the frontend**
   ```bash
   npm start
   ```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Database
DATABASE_URL=postgresql://footybets_user:footybets_password@localhost:5432/footybets

# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Scraping Configuration
SCRAPING_DELAY=1
USER_AGENT=Mozilla/5.0 (compatible; FootyBets/1.0)

# API Configuration
API_SECRET_KEY=your-secret-key-change-this-in-production

# AFL Tables URL
AFL_TABLES_URL=https://afltables.com.au

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000
```

## Getting Started

1. **Scrape historical data**
   - Go to http://localhost:3000/scraping
   - Click "Scrape Historical Data" to get the last 5 years of AFL data

2. **Generate predictions**
   - Go to http://localhost:3000/predictions
   - Click "Generate Predictions" to create AI predictions for upcoming games

3. **View analytics**
   - Go to http://localhost:3000/analytics
   - View prediction accuracy and performance metrics

## API Endpoints

### Games
- `GET /api/games` - Get all games
- `GET /api/games/upcoming` - Get upcoming games
- `GET /api/games/{id}` - Get specific game

### Predictions
- `GET /api/predictions` - Get all predictions
- `GET /api/predictions/upcoming` - Get upcoming predictions
- `POST /api/predictions/generate` - Generate new predictions
- `POST /api/predictions/update-accuracy` - Update prediction accuracy

### Analytics
- `GET /api/analytics/overview` - Get analytics overview
- `GET /api/analytics/team-performance` - Get team performance stats
- `GET /api/analytics/prediction-trends` - Get prediction trends

### Scraping
- `POST /api/scraping/historical-data` - Scrape historical data
- `POST /api/scraping/season` - Scrape specific season
- `GET /api/scraping/status` - Get scraping status

## Development Workflow

1. **Data Collection**
   - Use the scraping endpoints to collect historical AFL data
   - The scraper will automatically create teams and games

2. **AI Predictions**
   - Generate predictions for upcoming games
   - The AI uses Google Gemini to analyze historical data
   - Predictions include confidence scores and reasoning

3. **Analytics**
   - Track prediction accuracy over time
   - Analyze team performance
   - Monitor betting recommendations

## Troubleshooting

### Common Issues

1. **Database connection errors**
   - Ensure PostgreSQL is running
   - Check DATABASE_URL in .env
   - Verify database credentials

2. **API key errors**
   - Ensure GEMINI_API_KEY is set correctly
   - Check Google Gemini API quota

3. **Scraping errors**
   - Check internet connection
   - Verify AFL tables website is accessible
   - Adjust SCRAPING_DELAY if needed

4. **Frontend not loading**
   - Check REACT_APP_API_URL in frontend .env
   - Ensure backend is running on correct port
   - Check browser console for errors

### Logs

View logs for each service:
```bash
# Backend logs
docker-compose logs backend

# Frontend logs
docker-compose logs frontend

# Database logs
docker-compose logs postgres
```

## Production Deployment

For production deployment:

1. **Update environment variables**
   - Use strong API_SECRET_KEY
   - Set production database URL
   - Configure proper CORS origins

2. **Build production images**
   ```bash
   docker-compose -f docker-compose.prod.yml build
   ```

3. **Set up reverse proxy**
   - Configure Nginx for SSL termination
   - Set up domain and DNS

4. **Database backup**
   - Set up automated database backups
   - Configure database replication if needed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details 