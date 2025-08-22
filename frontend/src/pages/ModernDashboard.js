import React, { useState, useEffect } from 'react';
import { apiService } from '../services/apiService';
import { 
  TrophyIcon, 
  ChartBarIcon, 
  CalendarIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  SparklesIcon,
  FireIcon
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';
import SEO from '../components/SEO';

const ModernDashboard = () => {
  const [featuredTips, setFeaturedTips] = useState([]);
  const [weeklyTips, setWeeklyTips] = useState([]);
  const [accuracyStats, setAccuracyStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('featured');

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Load featured tips, weekly tips, and accuracy stats in parallel
      const [featuredResponse, weeklyResponse, accuracyResponse] = await Promise.all([
        apiService.get('/tips/featured?limit=3'),
        apiService.get('/tips/weekly'),
        apiService.get('/tips/accuracy?days_back=30')
      ]);

      setFeaturedTips(featuredResponse.data.featured_tips || []);
      setWeeklyTips(weeklyResponse.data.tips || []);
      setAccuracyStats(accuracyResponse.data.stats || {});
      
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 80) return 'text-green-600 bg-green-100';
    if (confidence >= 65) return 'text-blue-600 bg-blue-100';
    if (confidence >= 50) return 'text-yellow-600 bg-yellow-100';
    return 'text-gray-600 bg-gray-100';
  };

  const getConfidenceIcon = (confidence) => {
    if (confidence >= 80) return <FireIcon className="h-4 w-4" />;
    if (confidence >= 65) return <SparklesIcon className="h-4 w-4" />;
    if (confidence >= 50) return <CheckCircleIcon className="h-4 w-4" />;
    return <ExclamationTriangleIcon className="h-4 w-4" />;
  };

  const formatGameDate = (dateString) => {
    if (!dateString) return 'TBD';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-AU', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const TipCard = ({ tip, featured = false }) => {
    const prediction = tip.prediction || {};
    const confidence = prediction.confidence || 0;
    const betting = tip.betting_recommendation || {};

    return (
      <div className={`bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden transition-all duration-300 hover:shadow-xl hover:scale-105 ${featured ? 'border-l-4 border-l-blue-500' : ''}`}>
        {featured && (
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2">
            <div className="flex items-center space-x-2">
              <TrophyIcon className="h-5 w-5" />
              <span className="font-semibold">Featured Tip</span>
            </div>
          </div>
        )}
        
        <div className="p-6">
          {/* Match Header */}
          <div className="mb-4">
            <h3 className="text-xl font-bold text-gray-900 mb-2">
              {tip.match_title}
            </h3>
            <div className="flex items-center space-x-4 text-sm text-gray-600">
              <div className="flex items-center space-x-1">
                <CalendarIcon className="h-4 w-4" />
                <span>{formatGameDate(tip.game_date)}</span>
              </div>
              {tip.venue && (
                <div className="flex items-center space-x-1">
                  <span>📍</span>
                  <span>{tip.venue}</span>
                </div>
              )}
              {tip.round && (
                <div className="bg-gray-100 px-2 py-1 rounded-full text-xs font-medium">
                  Round {tip.round}
                </div>
              )}
            </div>
          </div>

          {/* Prediction */}
          {tip.has_prediction ? (
            <div className="space-y-4">
              {/* Winner & Confidence */}
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">Our Prediction</span>
                  <div className={`px-3 py-1 rounded-full text-xs font-semibold flex items-center space-x-1 ${getConfidenceColor(confidence)}`}>
                    {getConfidenceIcon(confidence)}
                    <span>{confidence}% confidence</span>
                  </div>
                </div>
                
                <div className="text-lg font-bold text-gray-900 mb-2">
                  {prediction.winner} to win
                </div>
                
                {prediction.predicted_score && (
                  <div className="flex items-center space-x-4 text-sm text-gray-600">
                    <span>Predicted Score:</span>
                    <span className="font-mono bg-white px-2 py-1 rounded">
                      {tip.home_team} {prediction.predicted_score.home} - {prediction.predicted_score.away} {tip.away_team}
                    </span>
                    {prediction.margin && (
                      <span className="text-blue-600 font-medium">
                        Margin: {prediction.margin} pts
                      </span>
                    )}
                  </div>
                )}
              </div>

              {/* Summary */}
              {tip.summary && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 className="font-semibold text-blue-900 mb-2">Quick Summary</h4>
                  <p className="text-blue-800" dangerouslySetInnerHTML={{ __html: tip.summary }} />
                </div>
              )}

              {/* Betting Recommendation */}
              {betting.recommendation && betting.recommendation !== "No recommendation" && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <h4 className="font-semibold text-green-900 mb-2">Betting Insight</h4>
                  <p className="text-green-800">{betting.recommendation}</p>
                  {betting.confidence && (
                    <div className="mt-2 text-sm text-green-700">
                      Betting confidence: {betting.confidence}%
                    </div>
                  )}
                </div>
              )}

              {/* AI Reasoning */}
              {prediction.reasoning && (
                <details className="bg-gray-50 rounded-lg p-4 cursor-pointer">
                  <summary className="font-semibold text-gray-900 mb-2">AI Analysis</summary>
                  <p className="text-gray-700 text-sm mt-2">{prediction.reasoning}</p>
                </details>
              )}
            </div>
          ) : (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-center">
              <ClockIcon className="h-8 w-8 text-yellow-600 mx-auto mb-2" />
              <p className="text-yellow-800 font-medium">Prediction coming soon</p>
              <p className="text-yellow-600 text-sm">Our AI is analyzing this match</p>
            </div>
          )}
        </div>
      </div>
    );
  };

  const StatsCard = ({ title, value, subtitle, icon: Icon, color = 'blue' }) => (
    <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className={`text-3xl font-bold text-${color}-600`}>{value}</p>
          {subtitle && <p className="text-sm text-gray-500 mt-1">{subtitle}</p>}
        </div>
        <div className={`bg-${color}-100 p-3 rounded-full`}>
          <Icon className={`h-8 w-8 text-${color}-600`} />
        </div>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your personalized AFL insights...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <SEO 
        title="AFL AI Tips Dashboard - FootyBets.ai"
        description="Your personalized AFL betting insights powered by AI. Get weekly tips, predictions, and analysis."
      />
      
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-blue-800 text-white">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-2">Your AFL AI Dashboard</h1>
            <p className="text-xl text-blue-100">Powered by advanced machine learning and data analysis</p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Stats Overview */}
        {accuracyStats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <StatsCard
              title="AI Accuracy"
              value={`${accuracyStats.accuracy_rate || 0}%`}
              subtitle="Last 30 days"
              icon={TrophyIcon}
              color="green"
            />
            <StatsCard
              title="Predictions Made"
              value={accuracyStats.total_predictions || 0}
              subtitle="Recent period"
              icon={ChartBarIcon}
              color="blue"
            />
            <StatsCard
              title="Correct Tips"
              value={accuracyStats.correct_predictions || 0}
              subtitle="Winning predictions"
              icon={CheckCircleIcon}
              color="purple"
            />
            <StatsCard
              title="Weekly Tips"
              value={weeklyTips.length}
              subtitle="This week"
              icon={CalendarIcon}
              color="indigo"
            />
          </div>
        )}

        {/* Featured Tips */}
        {featuredTips.length > 0 && (
          <div className="mb-8">
            <div className="flex items-center space-x-3 mb-6">
              <TrophyIcon className="h-8 w-8 text-yellow-500" />
              <h2 className="text-3xl font-bold text-gray-900">Featured Tips</h2>
              <div className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-medium">
                Highest Confidence
              </div>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
              {featuredTips.map((tip, index) => (
                <TipCard key={`featured-${tip.game_id}-${index}`} tip={tip} featured={true} />
              ))}
            </div>
          </div>
        )}

        {/* Navigation Tabs */}
        <div className="mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('featured')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'featured'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Featured Tips
              </button>
              <button
                onClick={() => setActiveTab('weekly')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'weekly'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                This Week ({weeklyTips.length})
              </button>
            </nav>
          </div>
        </div>

        {/* Weekly Tips */}
        {activeTab === 'weekly' && (
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">This Week's Tips</h2>
            
            {weeklyTips.length > 0 ? (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {weeklyTips.map((tip, index) => (
                  <TipCard key={`weekly-${tip.game_id}-${index}`} tip={tip} />
                ))}
              </div>
            ) : (
              <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-12 text-center">
                <CalendarIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No Tips Available</h3>
                <p className="text-gray-600 mb-4">Check back soon for this week's AFL predictions</p>
                <button
                  onClick={loadDashboardData}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Refresh
                </button>
              </div>
            )}
          </div>
        )}

        {/* Quick Actions */}
        <div className="mt-12 bg-white rounded-xl shadow-lg border border-gray-200 p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-left hover:bg-blue-100 transition-colors">
              <ChartBarIcon className="h-8 w-8 text-blue-600 mb-2" />
              <h4 className="font-semibold text-blue-900">View Analytics</h4>
              <p className="text-blue-700 text-sm">Detailed performance metrics</p>
            </button>
            
            <button className="bg-green-50 border border-green-200 rounded-lg p-4 text-left hover:bg-green-100 transition-colors">
              <CalendarIcon className="h-8 w-8 text-green-600 mb-2" />
              <h4 className="font-semibold text-green-900">View Fixtures</h4>
              <p className="text-green-700 text-sm">Upcoming AFL matches</p>
            </button>
            
            <button 
              onClick={loadDashboardData}
              className="bg-purple-50 border border-purple-200 rounded-lg p-4 text-left hover:bg-purple-100 transition-colors"
            >
              <SparklesIcon className="h-8 w-8 text-purple-600 mb-2" />
              <h4 className="font-semibold text-purple-900">Refresh Tips</h4>
              <p className="text-purple-700 text-sm">Get latest predictions</p>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModernDashboard; 