# FootyBets.ai - AI-Powered AFL Betting Predictions

An intelligent platform that uses AI to predict AFL game outcomes based on historical data and current team statistics.

![FootyBets.ai](https://img.shields.io/badge/FootyBets-AI%20Predictions-blue)
![React](https://img.shields.io/badge/React-18.2.0-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue)

## 🚀 Features

- **🤖 AI Predictions**: Google Gemini-powered game outcome predictions
- **📊 Data Scraping**: Automated scraping of AFL data from afltables.com.au
- **📈 Analytics Dashboard**: Track AI performance and betting results
- **🔄 Weekly Updates**: Automated predictions after team announcements
- **🔐 Security**: Comprehensive security with JWT authentication, rate limiting, and encryption
- **📱 Mobile Ready**: Designed to be adapted for iOS and Android apps
- **👥 User Management**: Role-based access control (Admin, Subscriber, User)

## 🛠️ Tech Stack

### Backend
- **Python FastAPI** - Modern, fast web framework
- **PostgreSQL** - Robust relational database
- **SQLAlchemy** - Database ORM
- **Google Gemini API** - AI predictions
- **BeautifulSoup/Scrapy** - Web scraping
- **JWT Authentication** - Secure user authentication
- **Redis** - Caching and rate limiting

### Frontend
- **React 18** - Modern UI framework
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **Recharts** - Data visualization
- **Framer Motion** - Animations
- **React Router** - Client-side routing

### Security
- **JWT Tokens** - Secure authentication
- **bcrypt** - Password hashing
- **Rate Limiting** - API protection
- **Input Validation** - XSS/SQL injection protection
- **CORS** - Cross-origin security
- **Security Headers** - HSTS, CSP, X-Frame-Options

## 📁 Project Structure

```
FootyBets.ai/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/routes/     # API endpoints
│   │   ├── core/           # Configuration & security
│   │   ├── models/         # Database models
│   │   ├── scrapers/       # Data scraping
│   │   └── ai/             # AI prediction logic
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Utility functions
│   ├── package.json        # Node.js dependencies
│   └── Dockerfile
├── mobile/                 # React Native app (coming soon)
├── docker-compose.yml      # Multi-service orchestration
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- PostgreSQL 13+
- Docker (optional)

### Frontend Setup
```bash
cd frontend
npm install
npm start
```
Visit: http://localhost:3000

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API: http://localhost:8000

### Environment Variables
Create `.env` files in both `backend/` and `frontend/` directories:

**Backend (.env)**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/footybets
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_secret_key
ENCRYPTION_KEY=your_encryption_key
```

**Frontend (.env)**
```env
REACT_APP_API_URL=http://localhost:8000
```

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Token refresh
- `POST /api/auth/logout` - User logout

### Predictions
- `GET /api/predictions` - Get AI predictions
- `POST /api/predictions/generate` - Generate new predictions
- `POST /api/predictions/update-accuracy` - Update accuracy

### Analytics
- `GET /api/analytics/overview` - Analytics overview
- `GET /api/analytics/team-performance` - Team performance stats
- `POST /api/analytics/generate-analytics` - Generate analytics

### Games
- `GET /api/games` - Get games
- `GET /api/games/upcoming` - Get upcoming games

### Admin
- `GET /api/admin/users` - User management
- `POST /api/admin/users/{id}/promote-admin` - Promote to admin
- `GET /api/admin/security-logs` - Security logs

## 🔐 Security Features

- **JWT Authentication** with refresh tokens
- **Role-based Access Control** (Admin, Subscriber, User)
- **Rate Limiting** on API endpoints
- **Account Lockout** after failed login attempts
- **Password Strength Validation**
- **Input Sanitization** and validation
- **SQL Injection Protection**
- **XSS Protection** with security headers
- **CORS Configuration**
- **Audit Logging** for security events

## 📱 Mobile App (Coming Soon)

The platform is designed to be easily adapted for mobile:
- **React Native** with Expo
- **Redux Toolkit** for state management
- **React Navigation** for routing
- **Expo SecureStore** for secure storage
- **Biometric Authentication**
- **Push Notifications**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the `/docs` endpoint when backend is running
- **Issues**: Create an issue on GitHub
- **Email**: support@footybets.ai

## 🔮 Roadmap

- [ ] Mobile app development
- [ ] Advanced analytics and insights
- [ ] User tip submission and comparison
- [ ] Real-time notifications
- [ ] Advanced AI model training
- [ ] Social features and leaderboards
- [ ] Integration with betting platforms
- [ ] Machine learning model improvements

---

**Disclaimer**: This platform is for educational and entertainment purposes only. Please gamble responsibly and be aware of the risks involved in sports betting. 