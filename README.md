# 🏈 FootyBets.ai - AI-Powered AFL Betting Predictions

An intelligent platform that uses AI to analyze AFL games and provide betting predictions with a witty, comedic tone that appeals to betting enthusiasts.

## 🚀 Live Demo

- **Frontend**: https://footybets-frontend-818397187963.us-central1.run.app
- **Backend API**: https://footybets-backend-818397187963.us-central1.run.app

## 🏗️ Architecture

- **Frontend**: React.js with modern UI/UX
- **Backend**: FastAPI (Python) with AI prediction engine
- **Database**: PostgreSQL on Google Cloud SQL
- **Deployment**: Google Cloud Run with automatic CI/CD
- **AI**: Google Gemini API for predictions and content generation

## 🎯 Features

- 🤖 **AI Predictions**: Machine learning models for game outcomes
- 📊 **Historical Analysis**: Comprehensive AFL statistics and trends
- 🏆 **Brownlow Medal Predictions**: AI-powered vote predictions
- 📱 **Mobile App**: React Native mobile application
- 🔄 **Real-time Updates**: Live game data and predictions
- 🎭 **Witty Content**: AI-generated comedic analysis and commentary

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **AI/ML**: Google Gemini API
- **Scraping**: BeautifulSoup, Selenium
- **Deployment**: Google Cloud Run

### Frontend
- **Framework**: React.js
- **Styling**: CSS3, modern responsive design
- **State Management**: React Context API
- **Deployment**: Google Cloud Run

### Mobile
- **Framework**: React Native
- **State Management**: Redux Toolkit
- **Notifications**: Push notifications

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Google Cloud CLI
- PostgreSQL

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/digitalimprov/footybets-ai.git
   cd footybets-ai
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Environment Variables**:
   Create `.env` files in both `backend/` and `frontend/` directories with:
   ```
   DATABASE_URL=postgresql://user:password@localhost/footybets
   GEMINI_API_KEY=your_gemini_api_key
   ```

## 🚀 Deployment

### Google Cloud Deployment

The application is automatically deployed to Google Cloud Platform using Cloud Build:

1. **Automatic Deployment**: Push to `main` branch triggers automatic deployment
2. **Manual Deployment**: Use `./deploy-update.sh` for immediate updates
3. **Infrastructure**: Managed by `cloudbuild.yaml` and deployment scripts

### Deployment URLs
- **Production**: https://footybets-frontend-818397187963.us-central1.run.app
- **API**: https://footybets-backend-818397187963.us-central1.run.app

## 📊 Database Schema

The application uses PostgreSQL with the following key tables:
- `games`: AFL game data and statistics
- `predictions`: AI-generated predictions
- `users`: User accounts and preferences
- `analytics`: Usage analytics and performance metrics

## 🤖 AI Features

### Prediction Engine
- **Game Outcomes**: Win/loss predictions with confidence scores
- **Player Performance**: Individual player statistics predictions
- **Brownlow Votes**: AI-powered Brownlow Medal vote predictions
- **Content Generation**: Witty, comedic analysis and commentary

### Data Sources
- **AFL Statistics**: Official AFL data and historical records
- **Brownlow Content**: Comprehensive Brownlow Medal analysis
- **Real-time Updates**: Live game data and statistics

## 🎭 Content Style

All AI-generated content follows a specific tone:
- **Smart & Witty**: Intelligent analysis with humor
- **Betting-Focused**: Tailored for AFL betting enthusiasts
- **Comedic**: Engaging and entertaining commentary
- **Professional**: Accurate predictions and analysis

## 📱 Mobile App

The React Native mobile app provides:
- **Push Notifications**: Real-time prediction updates
- **Offline Support**: Cached predictions and data
- **Native Performance**: Smooth, responsive interface
- **Cross-Platform**: iOS and Android support

## 🔧 Development Workflow

### Code Updates
1. **Edit in Cursor**: Make changes to your code
2. **Commit & Push**: `git add . && git commit -m "message" && git push`
3. **Automatic Deployment**: Cloud Build automatically deploys to production

### Testing
- **Backend**: FastAPI automatic API documentation at `/docs`
- **Frontend**: React development server with hot reload
- **Mobile**: React Native development build

## 📈 Analytics & Monitoring

- **Google Analytics**: User behavior and performance tracking
- **Cloud Monitoring**: Application performance and error tracking
- **Custom Analytics**: Betting prediction accuracy and user engagement

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- **Issues**: Create an issue on GitHub
- **Documentation**: Check the `/docs` endpoints for API documentation
- **Deployment**: Refer to `GITHUB_SETUP_GUIDE.md` for deployment setup

---

**🏈 Built with ❤️ for AFL betting enthusiasts** 