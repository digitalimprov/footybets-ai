import React, { useState, useEffect } from 'react';
import { 
  ChartBarIcon, 
  CalendarIcon, 
  ArrowTrendingUpIcon, 
  CogIcon,
  PlayIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { apiService } from '../services/apiService';
import toast from 'react-hot-toast';
import SEO from '../components/SEO';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalGames: 0,
    totalPredictions: 0,
    accuracy: 0,
    upcomingGames: 0
  });
  const [loading, setLoading] = useState(true);
  const [recentPredictions, setRecentPredictions] = useState([]);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Load analytics overview
      const analytics = await apiService.getAnalyticsOverview('all');
      
      // Load upcoming games
      const upcomingGames = await apiService.getUpcomingGames(7);
      
      // Load recent predictions
      const predictions = await apiService.getPredictions(10);
      
      setStats({
        totalGames: analytics.total_predictions || 0,
        totalPredictions: analytics.total_predictions || 0,
        accuracy: analytics.accuracy_percentage || 0,
        upcomingGames: upcomingGames.length || 0
      });
      
      setRecentPredictions(predictions.slice(0, 5));
      
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const generatePredictions = async () => {
    try {
      toast.loading('Generating predictions...');
      await apiService.generatePredictions(7);
      toast.success('Predictions generated successfully!');
      loadDashboardData(); // Refresh data
    } catch (error) {
      console.error('Error generating predictions:', error);
      toast.error('Failed to generate predictions');
    }
  };

  const scrapeData = async () => {
    try {
      toast.loading('Scraping AFL data...');
      await apiService.scrapeHistoricalData(2020, 2024);
      toast.success('Data scraping completed!');
      loadDashboardData(); // Refresh data
    } catch (error) {
      console.error('Error scraping data:', error);
      toast.error('Failed to scrape data');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="loading-spinner"></div>
      </div>
    );
  }

  return (
    <>
      <SEO 
        title="Dashboard"
        description="AI-powered AFL betting predictions dashboard. View real-time statistics, recent predictions, and upcoming games with expert analysis."
        keywords={['AFL betting', 'AI predictions', 'football tips', 'sports betting', 'AFL tips', 'betting predictions']}
        url="/"
        structuredData={{
          "@context": "https://schema.org",
          "@type": "WebPage",
          "name": "FootyBets.ai Dashboard",
          "description": "AI-powered AFL betting predictions dashboard",
          "url": "https://footybets.ai/",
          "mainEntity": {
            "@type": "Organization",
            "name": "FootyBets.ai",
            "description": "AI-powered AFL betting predictions"
          }
        }}
      />
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-600">AI-powered AFL betting predictions overview</p>
          </div>
          <div className="flex space-x-3">
            <button
              onClick={generatePredictions}
              className="btn-primary flex items-center"
            >
              <PlayIcon className="w-4 h-4 mr-2" />
              Generate Predictions
            </button>
            <button
              onClick={scrapeData}
              className="btn-secondary flex items-center"
            >
              <CogIcon className="w-4 h-4 mr-2" />
              Scrape Data
            </button>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="card">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <ChartBarIcon className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Predictions</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalPredictions}</p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <ArrowTrendingUpIcon className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Accuracy</p>
                <p className="text-2xl font-bold text-gray-900">{stats.accuracy.toFixed(1)}%</p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <CalendarIcon className="w-6 h-6 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Upcoming Games</p>
                <p className="text-2xl font-bold text-gray-900">{stats.upcomingGames}</p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <CheckCircleIcon className="w-6 h-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Games</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalGames}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Predictions */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Predictions</h2>
          {recentPredictions.length > 0 ? (
            <div className="space-y-4">
              {recentPredictions.map((prediction) => (
                <div key={prediction.id} className="border-b border-gray-200 pb-4 last:border-b-0">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-medium text-gray-900">
                        {prediction.home_team_name} vs {prediction.away_team_name}
                      </p>
                      <p className="text-sm text-gray-600">
                        Predicted: {prediction.predicted_winner_name} 
                        ({prediction.predicted_home_score}-{prediction.predicted_away_score})
                      </p>
                    </div>
                    <div className="text-right">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        prediction.confidence_score > 0.8 ? 'bg-green-100 text-green-800' :
                        prediction.confidence_score > 0.6 ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {(prediction.confidence_score * 100).toFixed(0)}% confidence
                      </span>
                      {prediction.is_correct !== null && (
                        <div className="mt-1">
                          <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium ${
                            prediction.is_correct ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                          }`}>
                            {prediction.is_correct ? 'Correct' : 'Incorrect'}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-8">No recent predictions available</p>
          )}
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
            <div className="space-y-3">
              <button
                onClick={generatePredictions}
                className="w-full btn-primary flex items-center justify-center"
              >
                <PlayIcon className="w-4 h-4 mr-2" />
                Generate New Predictions
              </button>
              <button
                onClick={scrapeData}
                className="w-full btn-secondary flex items-center justify-center"
              >
                <CogIcon className="w-4 h-4 mr-2" />
                Update Historical Data
              </button>
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">System Status</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">API Status</span>
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Online
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Database</span>
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Connected
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">AI Model</span>
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Active
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Dashboard; 