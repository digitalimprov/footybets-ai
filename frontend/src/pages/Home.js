import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import apiService from '../services/apiService';

const Home = () => {
  const [recentWins, setRecentWins] = useState([]);
  const [weeklyAnalytics, setWeeklyAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHomeData = async () => {
      try {
        // Fetch recent best wins (predictions with high confidence that were correct)
        const predictions = await apiService.getPredictions(10, { 
          is_correct: true, 
          confidence_score_min: 0.7 
        });
        
        // Get the most recent wins
        const wins = predictions.data.slice(0, 5);
        setRecentWins(wins);

        // Fetch weekly analytics
        const analytics = await apiService.getAnalyticsOverview('weekly');
        setWeeklyAnalytics(analytics.data);

      } catch (error) {
        console.error('Error fetching home data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchHomeData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <>
      <Helmet>
        <title>FootyBets.ai - AI-Powered AFL Betting Predictions</title>
        <meta name="description" content="Get AI-powered AFL betting predictions with witty analysis. Expert tips, analytics, and insights for AFL betting enthusiasts." />
        <meta name="keywords" content="AFL betting, football predictions, AI predictions, betting tips, AFL tips" />
        <link rel="canonical" href="https://footybets.ai" />
      </Helmet>

      <div className="min-h-screen">
        {/* Hero Section */}
        <section className="bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 text-white">
          <div className="container mx-auto px-4 py-20">
            <div className="text-center max-w-4xl mx-auto">
              <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-yellow-400 to-orange-400 bg-clip-text text-transparent">
                FootyBets.ai
              </h1>
              <p className="text-xl md:text-2xl mb-8 text-blue-100">
                AI-Powered AFL Betting Predictions with a Witty Twist
              </p>
              <p className="text-lg mb-12 text-blue-200 max-w-2xl mx-auto">
                Get intelligent predictions, expert analysis, and comedic commentary 
                that makes AFL betting both profitable and entertaining.
              </p>
              
              {/* Call to Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                <Link
                  to="/afl-betting-tips/upcoming"
                  className="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-bold py-4 px-8 rounded-lg text-lg transition-all duration-300 transform hover:scale-105 shadow-lg"
                >
                  🎯 Upcoming Tips
                </Link>
                <Link
                  to="/afl-analytics"
                  className="bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700 text-white font-bold py-4 px-8 rounded-lg text-lg transition-all duration-300 transform hover:scale-105 shadow-lg"
                >
                  📊 Past Results
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Recent Best Wins Section */}
        <section className="py-16 bg-gray-50">
          <div className="container mx-auto px-4">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                Recent Best Wins
              </h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Our AI's most confident predictions that delivered results
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {recentWins.map((win, index) => (
                <div key={win.id} className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-green-500">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="font-bold text-lg text-gray-900">
                        {win.home_team_name} vs {win.away_team_name}
                      </h3>
                      <p className="text-sm text-gray-600">
                        Round {win.game?.round_number} • {win.game?.season}
                      </p>
                    </div>
                    <div className="text-right">
                      <span className="inline-block bg-green-100 text-green-800 text-xs font-semibold px-2 py-1 rounded-full">
                        {Math.round(win.confidence_score * 100)}% Confidence
                      </span>
                    </div>
                  </div>
                  
                  <div className="mb-4">
                    <p className="text-sm text-gray-700 mb-2">
                      <strong>Prediction:</strong> {win.predicted_winner_name} to win
                    </p>
                    <p className="text-sm text-gray-700">
                      <strong>Score:</strong> {win.predicted_home_score} - {win.predicted_away_score}
                    </p>
                  </div>

                  <div className="text-xs text-gray-500">
                    {new Date(win.prediction_date).toLocaleDateString()}
                  </div>
                </div>
              ))}
            </div>

            {recentWins.length === 0 && (
              <div className="text-center py-12">
                <p className="text-gray-500 text-lg">No recent wins to display yet.</p>
                <p className="text-gray-400">Generate some predictions to see results here!</p>
              </div>
            )}
          </div>
        </section>

        {/* Weekly Analytics Snapshot */}
        <section className="py-16 bg-white">
          <div className="container mx-auto px-4">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                This Week's Analytics
              </h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Performance metrics and insights from our AI predictions
              </p>
            </div>

            {weeklyAnalytics ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-lg p-6 text-center">
                  <div className="text-3xl font-bold mb-2">
                    {weeklyAnalytics.total_predictions || 0}
                  </div>
                  <div className="text-blue-100">Total Predictions</div>
                </div>

                <div className="bg-gradient-to-br from-green-500 to-green-600 text-white rounded-lg p-6 text-center">
                  <div className="text-3xl font-bold mb-2">
                    {weeklyAnalytics.correct_predictions || 0}
                  </div>
                  <div className="text-green-100">Correct Predictions</div>
                </div>

                <div className="bg-gradient-to-br from-purple-500 to-purple-600 text-white rounded-lg p-6 text-center">
                  <div className="text-3xl font-bold mb-2">
                    {weeklyAnalytics.accuracy_percentage ? Math.round(weeklyAnalytics.accuracy_percentage) : 0}%
                  </div>
                  <div className="text-purple-100">Accuracy Rate</div>
                </div>

                <div className="bg-gradient-to-br from-orange-500 to-orange-600 text-white rounded-lg p-6 text-center">
                  <div className="text-3xl font-bold mb-2">
                    {weeklyAnalytics.average_confidence ? Math.round(weeklyAnalytics.average_confidence * 100) : 0}%
                  </div>
                  <div className="text-orange-100">Avg Confidence</div>
                </div>
              </div>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-500 text-lg">Analytics data not available yet.</p>
                <p className="text-gray-400">Generate predictions to see analytics here!</p>
              </div>
            )}
          </div>
        </section>

        {/* Features Section */}
        <section className="py-16 bg-gray-50">
          <div className="container mx-auto px-4">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                Why Choose FootyBets.ai?
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">🤖</span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">AI-Powered Predictions</h3>
                <p className="text-gray-600">
                  Advanced machine learning algorithms analyze historical data, 
                  team performance, and current form to generate accurate predictions.
                </p>
              </div>

              <div className="text-center">
                <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">📊</span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Comprehensive Analytics</h3>
                <p className="text-gray-600">
                  Detailed performance metrics, accuracy tracking, and insights 
                  to help you make informed betting decisions.
                </p>
              </div>

              <div className="text-center">
                <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">🎭</span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Witty Commentary</h3>
                <p className="text-gray-600">
                  Enjoy intelligent analysis with a comedic twist that makes 
                  AFL betting both profitable and entertaining.
                </p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </>
  );
};

export default Home; 