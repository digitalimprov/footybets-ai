import React, { useState, useEffect, useCallback } from 'react';
import { Link, useParams, useLocation } from 'react-router-dom';
import { 
  CalendarIcon, 
  ChartBarIcon,
  ArrowTrendingUpIcon,
  EyeIcon,
  TrophyIcon
} from '@heroicons/react/24/outline';
import { apiService } from '../services/apiService';
import toast from 'react-hot-toast';
import { format } from 'date-fns';
import SEO from '../components/SEO';
import { urlStructure, generateGameUrl, generateSEOTitle, generateSEODescription } from '../utils/urlStructure';

const Tips = () => {
  const { roundNumber, season, teamSlug } = useParams();
  const location = useLocation();
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedRound, setSelectedRound] = useState(null);
  const [rounds, setRounds] = useState([]);

  const loadPredictions = useCallback(async () => {
    try {
      setLoading(true);
      const data = await apiService.getPredictions(100); // Get more predictions
      setPredictions(data);
      
      // Extract unique rounds
      const uniqueRounds = [...new Set(data.map(p => p.game?.round_number))].sort((a, b) => b - a);
      setRounds(uniqueRounds);
      
      // Set selected round based on URL parameter or default to latest
      if (roundNumber) {
        setSelectedRound(parseInt(roundNumber));
      } else if (uniqueRounds.length > 0) {
        setSelectedRound(uniqueRounds[0]);
      }
    } catch (error) {
      console.error('Error loading predictions:', error);
      toast.error('Failed to load predictions');
    } finally {
      setLoading(false);
    }
  }, [roundNumber]);

  useEffect(() => {
    loadPredictions();
  }, [loadPredictions]);

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

  const getRoundPredictions = () => {
    if (!selectedRound) return [];
    let filteredPredictions = predictions.filter(p => p.game?.round_number === selectedRound);
    
    // Filter by team if teamSlug is provided
    if (teamSlug) {
      filteredPredictions = filteredPredictions.filter(p => 
        p.game?.home_team_name?.toLowerCase().replace(/\s+/g, '-') === teamSlug ||
        p.game?.away_team_name?.toLowerCase().replace(/\s+/g, '-') === teamSlug
      );
    }
    
    return filteredPredictions;
  };

  const getRoundStats = () => {
    const roundPreds = getRoundPredictions();
    const total = roundPreds.length;
    const highConfidence = roundPreds.filter(p => p.confidence_score > 0.8).length;
    const mediumConfidence = roundPreds.filter(p => p.confidence_score > 0.6 && p.confidence_score <= 0.8).length;
    const lowConfidence = roundPreds.filter(p => p.confidence_score <= 0.6).length;

    return { total, highConfidence, mediumConfidence, lowConfidence };
  };

  const getPageTitle = () => {
    if (teamSlug) {
      const teamName = teamSlug.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
      return `${teamName} AFL Betting Tips`;
    }
    if (roundNumber) {
      return `Round ${roundNumber} AFL Betting Tips`;
    }
    if (season) {
      return `${season} AFL Betting Tips`;
    }
    return 'AFL Betting Tips';
  };

  const getPageDescription = () => {
    if (teamSlug) {
      const teamName = teamSlug.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
      return `${teamName} AFL betting tips and predictions. Get expert analysis and AI predictions for ${teamName} games.`;
    }
    if (roundNumber) {
      return `Round ${roundNumber} AFL betting tips and predictions. AI-powered analysis with expert betting recommendations.`;
    }
    if (season) {
      return `${season} AFL betting tips and predictions. Get expert analysis and AI predictions for the ${season} season.`;
    }
    return 'Get AI-powered AFL betting tips and predictions organized by rounds. Expert analysis, confidence scores, and betting recommendations for every game.';
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="loading-spinner"></div>
      </div>
    );
  }

  const roundStats = getRoundStats();

  return (
    <>
      <SEO 
        title={getPageTitle()}
        description={getPageDescription()}
        keywords={['AFL betting tips', 'football predictions', 'sports betting tips', 'AFL round tips', 'betting recommendations', 'AI predictions']}
        url={location.pathname}
        structuredData={{
          "@context": "https://schema.org",
          "@type": "WebPage",
          "name": getPageTitle(),
          "description": getPageDescription(),
          "url": `https://footybets.ai${location.pathname}`,
          "mainEntity": {
            "@type": "ItemList",
            "name": "AFL Betting Tips",
            "description": "Round-based betting tips and predictions"
          }
        }}
      />
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{getPageTitle()}</h1>
            <p className="text-gray-600">AI predictions and betting recommendations by round</p>
          </div>
        </div>

        {/* Round Selector */}
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">Select Round</h2>
          <div className="flex flex-wrap gap-2">
            {rounds.map((round) => (
              <Link
                key={round}
                to={urlStructure.tips.round(round)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  selectedRound === round
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Round {round}
              </Link>
            ))}
          </div>
        </div>

        {/* Round Statistics */}
        {selectedRound && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="card text-center">
              <div className="text-2xl font-bold text-blue-600">{roundStats.total}</div>
              <div className="text-sm text-gray-600">Total Games</div>
            </div>
            <div className="card text-center">
              <div className="text-2xl font-bold text-green-600">{roundStats.highConfidence}</div>
              <div className="text-sm text-gray-600">High Confidence</div>
            </div>
            <div className="card text-center">
              <div className="text-2xl font-bold text-yellow-600">{roundStats.mediumConfidence}</div>
              <div className="text-sm text-gray-600">Medium Confidence</div>
            </div>
            <div className="card text-center">
              <div className="text-2xl font-bold text-red-600">{roundStats.lowConfidence}</div>
              <div className="text-sm text-gray-600">Low Confidence</div>
            </div>
          </div>
        )}

        {/* Predictions Grid */}
        {selectedRound && (
          <div className="space-y-4">
            <h2 className="text-xl font-semibold">Round {selectedRound} Predictions</h2>
            
            {getRoundPredictions().length === 0 ? (
              <div className="card text-center py-12">
                <p className="text-gray-500">No predictions available for this round</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {getRoundPredictions().map((prediction) => (
                  <div key={prediction.id} className="card hover:shadow-lg transition-shadow">
                    {/* Game Header */}
                    <div className="border-b border-gray-200 pb-3 mb-4">
                      <h3 className="font-semibold text-gray-900 mb-2">
                        {prediction.game?.home_team_name} vs {prediction.game?.away_team_name}
                      </h3>
                      <div className="flex items-center text-sm text-gray-600">
                        <CalendarIcon className="w-4 h-4 mr-1" />
                        {prediction.game?.game_date && format(new Date(prediction.game.game_date), 'MMM d, yyyy')}
                      </div>
                    </div>

                    {/* Prediction Details */}
                    <div className="space-y-3">
                      {/* Predicted Winner */}
                      <div className="text-center">
                        <p className="text-sm text-gray-600 mb-1">Predicted Winner</p>
                        <p className="font-semibold text-gray-900">
                          {prediction.predicted_winner_name}
                        </p>
                      </div>

                      {/* Confidence */}
                      <div className="text-center">
                        <p className="text-sm text-gray-600 mb-1">Confidence</p>
                        <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getConfidenceColor(prediction.confidence_score)}`}>
                          <ArrowTrendingUpIcon className="w-3 h-3 mr-1" />
                          {(prediction.confidence_score * 100).toFixed(1)}%
                        </div>
                      </div>

                      {/* Predicted Score */}
                      <div className="text-center p-3 bg-gray-50 rounded-lg">
                        <p className="text-sm text-gray-600 mb-1">Predicted Score</p>
                        <p className="text-lg font-bold text-gray-900">
                          {prediction.predicted_home_score} - {prediction.predicted_away_score}
                        </p>
                      </div>

                      {/* Betting Tip */}
                      <div className="text-center">
                        <p className="text-sm text-gray-600 mb-2">Betting Tip</p>
                        <div className={`inline-flex items-center px-3 py-1 rounded-lg border text-sm font-medium ${getBetRecommendationColor(prediction.recommended_bet)}`}>
                          <span className="capitalize">
                            {prediction.recommended_bet === 'home' ? prediction.game?.home_team_name : 
                             prediction.recommended_bet === 'away' ? prediction.game?.away_team_name : 
                             prediction.recommended_bet}
                          </span>
                        </div>
                        <p className="text-xs text-gray-500 mt-1">
                          {(prediction.bet_confidence * 100).toFixed(1)}% confidence
                        </p>
                      </div>

                      {/* Game Status */}
                      {prediction.game?.is_finished && (
                        <div className="text-center p-2 bg-green-50 rounded-lg">
                          <div className="flex items-center justify-center text-green-700">
                            <TrophyIcon className="w-4 h-4 mr-1" />
                            <span className="text-sm font-medium">Game Finished</span>
                          </div>
                          <p className="text-xs text-green-600 mt-1">
                            {prediction.game.home_score} - {prediction.game.away_score}
                          </p>
                        </div>
                      )}

                      {/* View Details Button */}
                      <div className="pt-3 border-t border-gray-200">
                        <Link
                          to={generateGameUrl(prediction.game) || `/games/${prediction.game_id}`}
                          className="w-full btn-secondary flex items-center justify-center"
                        >
                          <EyeIcon className="w-4 h-4 mr-2" />
                          View Details
                        </Link>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* No Round Selected */}
        {!selectedRound && (
          <div className="card text-center py-12">
            <ChartBarIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No Predictions Available</h3>
            <p className="text-gray-600">Select a round to view AI predictions and betting tips.</p>
          </div>
        )}
      </div>
    </>
  );
};

export default Tips; 