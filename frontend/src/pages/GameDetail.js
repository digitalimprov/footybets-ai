import React, { useState, useEffect } from 'react';
import { useParams, Link, useLocation } from 'react-router-dom';
import { 
  CalendarIcon, 
  MapPinIcon, 
  TrophyIcon,
  ArrowTrendingUpIcon,
  ChartBarIcon,
  ClockIcon
} from '@heroicons/react/24/outline';
import { apiService } from '../services/apiService';
import toast from 'react-hot-toast';
import { format } from 'date-fns';
import SEO from '../components/SEO';
import { urlStructure, generateSEOTitle, generateSEODescription } from '../utils/urlStructure';

const GameDetail = () => {
  const { gameId, homeTeam, awayTeam, round, season } = useParams();
  const location = useLocation();
  const [game, setGame] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadGameData();
  }, [gameId, homeTeam, awayTeam, round, season]);

  const loadGameData = async () => {
    try {
      setLoading(true);
      
      // If we have URL parameters, try to find the game by teams and round
      let gameData = null;
      let predictionData = null;
      
      if (homeTeam && awayTeam && round && season) {
        // Try to find game by URL parameters first
        const games = await apiService.getGames();
        gameData = games.find(g => {
          const gHomeTeam = g.home_team_name?.toLowerCase().replace(/\s+/g, '-');
          const gAwayTeam = g.away_team_name?.toLowerCase().replace(/\s+/g, '-');
          return gHomeTeam === homeTeam && gAwayTeam === awayTeam && 
                 g.round_number === parseInt(round) && g.season === parseInt(season);
        });
        
        if (gameData) {
          predictionData = await apiService.getPredictionByGame(gameData.id);
        }
      } else if (gameId) {
        // Fallback to gameId
        [gameData, predictionData] = await Promise.all([
          apiService.getGame(gameId),
          apiService.getPredictionByGame(gameId)
        ]);
      }
      
      setGame(gameData);
      setPrediction(predictionData);
    } catch (error) {
      console.error('Error loading game data:', error);
      toast.error('Failed to load game data');
    } finally {
      setLoading(false);
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence > 0.8) return 'text-green-600 bg-green-100';
    if (confidence > 0.6) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getBetRecommendationColor = (recommendation) => {
    switch (recommendation) {
      case 'home':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'away':
        return 'bg-purple-100 text-purple-800 border-purple-200';
      case 'draw':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getSEOTitle = () => {
    if (game) {
      return generateSEOTitle('game', {
        homeTeam: game.home_team_name,
        awayTeam: game.away_team_name,
        round: game.round_number,
        season: game.season
      });
    }
    return 'AFL Game Prediction & Betting Tips';
  };

  const getSEODescription = () => {
    if (game) {
      return generateSEODescription('game', {
        homeTeam: game.home_team_name,
        awayTeam: game.away_team_name,
        round: game.round_number,
        season: game.season
      });
    }
    return 'Get AI-powered AFL predictions and betting tips. Expert analysis, predicted scores, and betting recommendations.';
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="loading-spinner"></div>
      </div>
    );
  }

  if (!game) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Game Not Found</h2>
        <p className="text-gray-600 mb-6">The game you're looking for doesn't exist.</p>
        <Link to={urlStructure.games.index} className="btn-primary">
          Back to Fixtures
        </Link>
      </div>
    );
  }

  return (
    <>
      <SEO 
        title={getSEOTitle()}
        description={getSEODescription()}
        keywords={game ? [`${game.home_team_name}`, `${game.away_team_name}`, 'AFL betting', 'football prediction', 'sports betting tips'] : ['AFL betting', 'football prediction']}
        url={location.pathname}
        type="article"
        publishedTime={game?.game_date}
        structuredData={game ? {
          "@context": "https://schema.org",
          "@type": "SportsEvent",
          "name": `${game.home_team_name} vs ${game.away_team_name}`,
          "description": `AFL Round ${game.round_number} game between ${game.home_team_name} and ${game.away_team_name}`,
          "startDate": game.game_date,
          "location": {
            "@type": "Place",
            "name": game.venue
          },
          "competitor": [
            {
              "@type": "SportsTeam",
              "name": game.home_team_name
            },
            {
              "@type": "SportsTeam", 
              "name": game.away_team_name
            }
          ]
        } : null}
      />
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              {game.home_team_name} vs {game.away_team_name}
            </h1>
            <p className="text-gray-600 mt-2">
              Round {game.round_number} • Season {game.season}
            </p>
          </div>
          <Link to={urlStructure.games.index} className="btn-secondary">
            Back to Fixtures
          </Link>
        </div>

        {/* Game Details */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Game Info */}
          <div className="lg:col-span-2">
            <div className="card">
              <h2 className="text-xl font-semibold mb-4">Game Information</h2>
              <div className="space-y-4">
                <div className="flex items-center">
                  <CalendarIcon className="w-5 h-5 text-gray-400 mr-3" />
                  <span className="text-gray-600">
                    {format(new Date(game.game_date), 'EEEE, MMMM d, yyyy')}
                  </span>
                </div>
                <div className="flex items-center">
                  <ClockIcon className="w-5 h-5 text-gray-400 mr-3" />
                  <span className="text-gray-600">
                    {format(new Date(game.game_date), 'h:mm a')}
                  </span>
                </div>
                <div className="flex items-center">
                  <MapPinIcon className="w-5 h-5 text-gray-400 mr-3" />
                  <span className="text-gray-600">{game.venue}</span>
                </div>
                {game.is_finished && (
                  <div className="flex items-center">
                    <TrophyIcon className="w-5 h-5 text-gray-400 mr-3" />
                    <span className="text-gray-600">
                      Final Score: {game.home_score} - {game.away_score}
                    </span>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* AI Prediction */}
          <div className="lg:col-span-1">
            <div className="card">
              <h2 className="text-xl font-semibold mb-4 flex items-center">
                <ChartBarIcon className="w-5 h-5 mr-2" />
                AI Prediction
              </h2>
              
              {prediction ? (
                <div className="space-y-4">
                  {/* Predicted Winner */}
                  <div className="text-center p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600 mb-2">Predicted Winner</p>
                    <p className="text-lg font-semibold text-gray-900">
                      {prediction.predicted_winner_name}
                    </p>
                  </div>

                  {/* Confidence Score */}
                  <div className="text-center">
                    <p className="text-sm text-gray-600 mb-2">Confidence</p>
                    <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getConfidenceColor(prediction.confidence_score)}`}>
                      <ArrowTrendingUpIcon className="w-4 h-4 mr-1" />
                      {(prediction.confidence_score * 100).toFixed(1)}%
                    </div>
                  </div>

                  {/* Predicted Score */}
                  <div className="text-center p-4 bg-blue-50 rounded-lg">
                    <p className="text-sm text-gray-600 mb-2">Predicted Score</p>
                    <p className="text-xl font-bold text-gray-900">
                      {prediction.predicted_home_score} - {prediction.predicted_away_score}
                    </p>
                  </div>

                  {/* Betting Recommendation */}
                  <div className="text-center">
                    <p className="text-sm text-gray-600 mb-2">Betting Tip</p>
                    <div className={`inline-flex items-center px-3 py-2 rounded-lg border ${getBetRecommendationColor(prediction.recommended_bet)}`}>
                      <span className="font-medium capitalize">
                        {prediction.recommended_bet === 'home' ? game.home_team_name : 
                         prediction.recommended_bet === 'away' ? game.away_team_name : 
                         prediction.recommended_bet}
                      </span>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">
                      {(prediction.bet_confidence * 100).toFixed(1)}% confidence
                    </p>
                  </div>

                  {/* AI Reasoning */}
                  <div className="mt-4">
                    <p className="text-sm font-medium text-gray-700 mb-2">AI Reasoning</p>
                    <p className="text-sm text-gray-600 leading-relaxed">
                      {prediction.reasoning}
                    </p>
                  </div>
                </div>
              ) : (
                <div className="text-center py-8">
                  <p className="text-gray-500">No AI prediction available yet</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Factors Considered */}
        {prediction && prediction.factors_considered && (
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Factors Considered</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {prediction.factors_considered.map((factor, index) => (
                <div key={index} className="flex items-center p-3 bg-gray-50 rounded-lg">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                  <span className="text-gray-700">{factor}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Odds Analysis */}
        {prediction && prediction.odds_analysis && (
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Odds Analysis</h2>
            <div className="bg-gray-50 p-4 rounded-lg">
              <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                {prediction.odds_analysis}
              </pre>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default GameDetail; 