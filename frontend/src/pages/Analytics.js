import React, { useState, useEffect } from 'react';
import {
  ChartBarIcon,
  ArrowTrendingUpIcon,
  CalendarIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline';
import apiService from '../services/apiService';
import toast from 'react-hot-toast';
import SEO from '../components/SEO';

const Analytics = () => {
  const [analytics, setAnalytics] = useState(null);
  const [teamPerformance, setTeamPerformance] = useState([]);
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState('all');

  useEffect(() => {
    loadAnalytics();
  }, [period]);

  const loadAnalytics = async () => {
    try {
      setLoading(true);

      const [analyticsData, teamData, trendsData] = await Promise.all([
        apiService.getAnalyticsOverview(period),
        apiService.getTeamPerformance(),
        apiService.getPredictionTrends(30)
      ]);

      setAnalytics(analyticsData);
      setTeamPerformance(teamData);
      setTrends(trendsData);

    } catch (error) {
      console.error('Error loading analytics:', error);
      toast.error('Failed to load analytics data');
    } finally {
      setLoading(false);
    }
  };

  const generateAnalytics = async () => {
    try {
      toast.loading('Generating analytics...');
      await apiService.generateAnalytics('weekly');
      toast.success('Analytics generated successfully!');
      loadAnalytics();
    } catch (error) {
      console.error('Error generating analytics:', error);
      toast.error('Failed to generate analytics');
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
        title="Analytics"
        description="Track AI prediction performance and betting analytics. View accuracy rates, trends, and detailed performance metrics for AFL betting predictions."
        keywords={['AFL analytics', 'betting analytics', 'prediction accuracy', 'sports betting stats', 'AFL performance metrics', 'betting trends']}
        url="/analytics"
        structuredData={{
          "@context": "https://schema.org",
          "@type": "WebPage",
          "name": "Analytics",
          "description": "AI prediction performance and betting analytics",
          "url": "https://footybets.ai/analytics",
          "mainEntity": {
            "@type": "Dataset",
            "name": "AFL Betting Analytics",
            "description": "Performance metrics and analytics for AFL predictions"
          }
        }}
      />
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
            <p className="text-gray-600">Track AI prediction performance and trends</p>
          </div>
          <div className="flex space-x-3">
            <select
              value={period}
              onChange={(e) => setPeriod(e.target.value)}
              className="input-field w-auto"
            >
              <option value="all">All Time</option>
              <option value="season">This Season</option>
              <option value="month">Last Month</option>
              <option value="week">Last Week</option>
            </select>
            <button
              onClick={generateAnalytics}
              className="btn-primary flex items-center"
            >
              <ArrowPathIcon className="w-4 h-4 mr-2" />
              Generate Analytics
            </button>
          </div>
        </div>

        {/* Overview Stats */}
        {analytics && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="card">
              <div className="flex items-center">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <ChartBarIcon className="w-6 h-6 text-blue-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Predictions</p>
                  <p className="text-2xl font-bold text-gray-900">{analytics.total_predictions}</p>
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
                  <p className="text-2xl font-bold text-gray-900">{analytics.accuracy_percentage.toFixed(1)}%</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <div className="p-2 bg-yellow-100 rounded-lg">
                  <CalendarIcon className="w-6 h-6 text-yellow-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Bets Recommended</p>
                  <p className="text-2xl font-bold text-gray-900">{analytics.total_bets_recommended}</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <ArrowTrendingUpIcon className="w-6 h-6 text-purple-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">ROI</p>
                  <p className="text-2xl font-bold text-gray-900">{analytics.betting_roi.toFixed(1)}%</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Confidence Breakdown */}
        {analytics && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Confidence Level Performance</h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-600">High Confidence (>80%)</span>
                  <span className="text-sm font-bold text-green-600">
                    {analytics.high_confidence_accuracy.toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-green-600 h-2 rounded-full"
                    style={{ width: `${analytics.high_confidence_accuracy}%` }}
                  ></div>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-600">Medium Confidence (60-80%)</span>
                  <span className="text-sm font-bold text-yellow-600">
                    {analytics.medium_confidence_accuracy.toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-yellow-600 h-2 rounded-full"
                    style={{ width: `${analytics.medium_confidence_accuracy}%` }}
                  ></div>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-600">Low Confidence (&lt;60%)</span>
                  <span className="text-sm font-bold text-red-600">
                    {analytics.low_confidence_accuracy.toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-red-600 h-2 rounded-full"
                    style={{ width: `${analytics.low_confidence_accuracy}%` }}
                  ></div>
                </div>
              </div>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Betting Performance</h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-600">Total Bets</span>
                  <span className="text-sm font-bold text-gray-900">{analytics.total_bets_recommended}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-600">Winning Bets</span>
                  <span className="text-sm font-bold text-green-600">{analytics.winning_bets}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-600">Win Rate</span>
                  <span className="text-sm font-bold text-blue-600">
                    {analytics.total_bets_recommended > 0
                      ? ((analytics.winning_bets / analytics.total_bets_recommended) * 100).toFixed(1)
                      : 0}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-600">ROI</span>
                  <span className={`text-sm font-bold ${analytics.betting_roi >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {analytics.betting_roi.toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Team Performance */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Team Performance</h3>
          {teamPerformance.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Team
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Games
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Wins
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Losses
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Win %
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Avg Score For
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Avg Score Against
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {teamPerformance.slice(0, 10).map((team, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {team.team_name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {team.total_games}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {team.wins}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {team.losses}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {team.win_percentage.toFixed(1)}%
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {team.avg_score_for.toFixed(1)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {team.avg_score_against.toFixed(1)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-gray-500 text-center py-8">No team performance data available</p>
          )}
        </div>

        {/* Prediction Trends */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Prediction Trends (Last 30 Days)</h3>
          {trends.length > 0 ? (
            <div className="space-y-4">
              {trends.map((trend, index) => (
                <div key={index} className="border-b border-gray-200 pb-4 last:border-b-0">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-900">{trend.date}</span>
                    <span className="text-sm font-bold text-blue-600">{trend.accuracy_percentage.toFixed(1)}%</span>
                  </div>
                  <div className="flex justify-between text-xs text-gray-500">
                    <span>{trend.total_predictions} predictions</span>
                    <span>{trend.correct_predictions} correct</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${trend.accuracy_percentage}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-8">No trend data available</p>
          )}
        </div>
      </div>
    </>
  );
};

export default Analytics; 