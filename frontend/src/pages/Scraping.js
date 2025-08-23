import React, { useState, useEffect } from 'react';
import {
  CogIcon,
  PlayIcon,
  ArrowPathIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import apiService from '../services/apiService';
import toast from 'react-hot-toast';
import SEO from '../components/SEO';

const Scraping = () => {
  const [status, setStatus] = useState(null);
  const [scraping, setScraping] = useState(false);
  const [startSeason, setStartSeason] = useState(2020);
  const [endSeason, setEndSeason] = useState(2024);

  useEffect(() => {
    loadStatus();
  }, []);

  const loadStatus = async () => {
    try {
      const data = await apiService.getScrapingStatus();
      setStatus(data);
    } catch (error) {
      console.error('Error loading scraping status:', error);
      toast.error('Failed to load scraping status');
    }
  };

  const scrapeHistoricalData = async () => {
    try {
      setScraping(true);
      toast.loading('Scraping historical AFL data...');
      await apiService.scrapeHistoricalData(startSeason, endSeason);
      toast.success('Historical data scraping completed!');
      loadStatus();
    } catch (error) {
      console.error('Error scraping historical data:', error);
      toast.error('Failed to scrape historical data');
    } finally {
      setScraping(false);
    }
  };

  const scrapeUpcomingGames = async () => {
    try {
      setScraping(true);
      toast.loading('Scraping upcoming games...');
      await apiService.scrapeUpcomingGames();
      toast.success('Upcoming games scraping completed!');
      loadStatus();
    } catch (error) {
      console.error('Error scraping upcoming games:', error);
      toast.error('Failed to scrape upcoming games');
    } finally {
      setScraping(false);
    }
  };

  const cleanupData = async () => {
    try {
      toast.loading('Cleaning up duplicate data...');
      await apiService.cleanupData();
      toast.success('Data cleanup completed!');
      loadStatus();
    } catch (error) {
      console.error('Error cleaning up data:', error);
      toast.error('Failed to cleanup data');
    }
  };

  return (
    <>
      <SEO
        title="Data Scraping"
        description="Admin data scraping interface"
        noindex={true}
        nofollow={true}
      />
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Data Scraping</h1>
            <p className="text-gray-600">Manage AFL data collection and updates</p>
          </div>
          <button
            onClick={loadStatus}
            className="btn-secondary flex items-center"
          >
            <ArrowPathIcon className="w-4 h-4 mr-2" />
            Refresh Status
          </button>
        </div>

        {/* Status Overview */}
        {status && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="card">
              <div className="flex items-center">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <CogIcon className="w-6 h-6 text-blue-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Games</p>
                  <p className="text-2xl font-bold text-gray-900">{status.total_games}</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <div className="p-2 bg-green-100 rounded-lg">
                  <CheckCircleIcon className="w-6 h-6 text-green-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Teams</p>
                  <p className="text-2xl font-bold text-gray-900">{status.total_teams}</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <div className="p-2 bg-yellow-100 rounded-lg">
                  <ExclamationTriangleIcon className="w-6 h-6 text-yellow-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Seasons Available</p>
                  <p className="text-2xl font-bold text-gray-900">{status.seasons_available?.length || 0}</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <ArrowPathIcon className="w-6 h-6 text-purple-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Last Updated</p>
                  <p className="text-sm font-bold text-gray-900">
                    {status.recent_games?.length > 0
                      ? new Date(status.recent_games[0].created_at).toLocaleDateString()
                      : 'Never'
                    }
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Scraping Actions */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Historical Data Scraping</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Start Season
                </label>
                <input
                  type="number"
                  value={startSeason}
                  onChange={(e) => setStartSeason(parseInt(e.target.value))}
                  className="input-field"
                  min="1990"
                  max="2030"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  End Season
                </label>
                <input
                  type="number"
                  value={endSeason}
                  onChange={(e) => setEndSeason(parseInt(e.target.value))}
                  className="input-field"
                  min="1990"
                  max="2030"
                />
              </div>
              <button
                onClick={scrapeHistoricalData}
                disabled={scraping}
                className="w-full btn-primary flex items-center justify-center"
              >
                {scraping ? (
                  <div className="loading-spinner w-4 h-4 mr-2"></div>
                ) : (
                  <PlayIcon className="w-4 h-4 mr-2" />
                )}
                {scraping ? 'Scraping...' : 'Scrape Historical Data'}
              </button>
              <p className="text-xs text-gray-500">
                This will scrape all AFL games from {startSeason} to {endSeason} from afltables.com.au
              </p>
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
            <div className="space-y-4">
              <button
                onClick={scrapeUpcomingGames}
                disabled={scraping}
                className="w-full btn-secondary flex items-center justify-center"
              >
                <PlayIcon className="w-4 h-4 mr-2" />
                Scrape Upcoming Games
              </button>

              <button
                onClick={cleanupData}
                className="w-full btn-danger flex items-center justify-center"
              >
                <ArrowPathIcon className="w-4 h-4 mr-2" />
                Cleanup Duplicate Data
              </button>

              <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
                <div className="flex">
                  <ExclamationTriangleIcon className="w-5 h-5 text-yellow-400" />
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-yellow-800">
                      Important Notes
                    </h3>
                    <div className="mt-2 text-sm text-yellow-700">
                      <ul className="list-disc list-inside space-y-1">
                        <li>Scraping may take several minutes for large date ranges</li>
                        <li>Be respectful of the AFL website's resources</li>
                        <li>Data is automatically deduplicated</li>
                        <li>Teams are created automatically as needed</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Season Breakdown */}
        {status?.season_breakdown && (
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Season Breakdown</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Season
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Games
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {status.season_breakdown.map((season) => (
                    <tr key={season.season} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {season.season}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {season.games}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Recent Activity */}
        {status?.recent_games && status.recent_games.length > 0 && (
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
            <div className="space-y-3">
              {status.recent_games.slice(0, 5).map((game) => (
                <div key={game.id} className="flex justify-between items-center py-2 border-b border-gray-100 last:border-b-0">
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {game.home_team} vs {game.away_team}
                    </p>
                    <p className="text-xs text-gray-500">
                      {new Date(game.created_at).toLocaleString()}
                    </p>
                  </div>
                  <span className="text-xs text-gray-500">
                    Season {new Date(game.game_date).getFullYear()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default Scraping; 