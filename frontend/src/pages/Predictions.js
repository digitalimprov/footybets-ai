import React, { useState, useEffect } from 'react';
import { PlayIcon, ArrowPathIcon, EyeIcon } from '@heroicons/react/24/outline';
import apiService from '../services/apiService';
import toast from 'react-hot-toast';
import SEO from '../components/SEO';
import { format } from 'date-fns';

const Predictions = () => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [selectedPrediction, setSelectedPrediction] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    loadPredictions();
  }, []);

  const loadPredictions = async () => {
    try {
      setLoading(true);
      const data = await apiService.getPredictions(50);
      setPredictions(data);
    } catch (error) {
      console.error('Error loading predictions:', error);
      
      // If backend is unavailable, use mock data
      if (error.response?.status === 405 || error.response?.status === 500 || !error.response) {
        const mockPredictions = [
          {
            id: 1,
            game_id: 1,
            home_team_name: "Richmond Tigers",
            away_team_name: "Collingwood Magpies",
            predicted_winner_name: "Richmond Tigers",
            confidence_score: 78.5,
            predicted_home_score: 95,
            predicted_away_score: 82,
            reasoning: "Richmond's home ground advantage and recent form suggest they're favored. Their midfield has been dominant in recent weeks, particularly around stoppages. Collingwood's injury list includes key defenders which could be exploited.",
            factors_considered: ["Home ground advantage", "Recent form", "Head-to-head record", "Injury reports", "Weather conditions"],
            recommended_bet: "Richmond 1-39 points",
            bet_confidence: 72.0,
            model_version: "AFL_Predictor_v2.1",
            prediction_date: new Date().toISOString(),
            is_correct: null
          },
          {
            id: 2,
            game_id: 2,
            home_team_name: "Melbourne Demons",
            away_team_name: "Brisbane Lions",
            predicted_winner_name: "Melbourne Demons",
            confidence_score: 82.3,
            predicted_home_score: 103,
            predicted_away_score: 78,
            reasoning: "Melbourne's defensive structure has been exceptional this season, allowing the fewest points per game. Brisbane's away form has been inconsistent, particularly against top-4 teams.",
            factors_considered: ["Defensive efficiency", "Away form", "Forward line effectiveness", "Ruck dominance"],
            recommended_bet: "Melbourne 40+ points",
            bet_confidence: 68.5,
            model_version: "AFL_Predictor_v2.1",
            prediction_date: new Date(Date.now() - 3600000).toISOString(),
            is_correct: null
          },
          {
            id: 3,
            game_id: 3,
            home_team_name: "Geelong Cats",
            away_team_name: "Western Bulldogs",
            predicted_winner_name: "Geelong Cats",
            confidence_score: 71.2,
            predicted_home_score: 89,
            predicted_away_score: 85,
            reasoning: "This is expected to be a close contest. Geelong's experience in big games gives them a slight edge, but the Bulldogs' pace could trouble them in transition.",
            factors_considered: ["Experience in finals", "Transition game", "Contested possession rate", "Goal kicking accuracy"],
            recommended_bet: "Under 174.5 total points",
            bet_confidence: 65.0,
            model_version: "AFL_Predictor_v2.1",
            prediction_date: new Date(Date.now() - 7200000).toISOString(),
            is_correct: null
          },
          {
            id: 4,
            game_id: 4,
            home_team_name: "Port Adelaide Power",
            away_team_name: "Sydney Swans",
            predicted_winner_name: "Sydney Swans",
            confidence_score: 69.8,
            predicted_home_score: 78,
            predicted_away_score: 91,
            reasoning: "Sydney's improved defensive pressure and ball movement efficiency make them favorites despite playing away. Port Adelaide's inconsistent goal kicking could prove costly.",
            factors_considered: ["Defensive pressure rating", "Ball movement efficiency", "Goal kicking accuracy", "Interstate travel"],
            recommended_bet: "Sydney -15.5 points",
            bet_confidence: 63.2,
            model_version: "AFL_Predictor_v2.1",
            prediction_date: new Date(Date.now() - 10800000).toISOString(),
            is_correct: null
          }
        ];
        
        setPredictions(mockPredictions);
        toast.warning('Backend unavailable - showing sample predictions for demonstration');
      } else {
        toast.error('Failed to load predictions');
      }
    } finally {
      setLoading(false);
    }
  };

  const generatePredictions = async () => {
    try {
      setGenerating(true);
      toast.loading('Generating predictions...');
      await apiService.generatePredictions(7);
      toast.success('Predictions generated successfully!');
      loadPredictions(); // Refresh the list
    } catch (error) {
      console.error('Error generating predictions:', error);
      if (error.response?.status === 405 || error.response?.status === 500 || !error.response) {
        toast.error('Prediction generation unavailable - backend not accessible');
      } else {
        toast.error('Failed to generate predictions');
      }
    } finally {
      setGenerating(false);
    }
  };

  const updateAccuracy = async () => {
    try {
      toast.loading('Updating prediction accuracy...');
      await apiService.updatePredictionAccuracy();
      toast.success('Accuracy updated successfully!');
      loadPredictions(); // Refresh the list
    } catch (error) {
      console.error('Error updating accuracy:', error);
      if (error.response?.status === 405 || error.response?.status === 500 || !error.response) {
        toast.error('Accuracy update unavailable - backend not accessible');
      } else {
        toast.error('Failed to update accuracy');
      }
    }
  };

  const viewPredictionDetails = (prediction) => {
    setSelectedPrediction(prediction);
    setShowModal(true);
  };

  const getConfidenceColor = (confidence) => {
    if (confidence > 0.8) return 'confidence-high';
    if (confidence > 0.6) return 'confidence-medium';
    return 'confidence-low';
  };

  const getBetRecommendationColor = (recommendation) => {
    switch (recommendation) {
      case 'home':
        return 'bg-blue-100 text-blue-800';
      case 'away':
        return 'bg-purple-100 text-purple-800';
      case 'draw':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
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
        title="AI Predictions"
        description="View AI-generated AFL predictions and betting tips. Get expert analysis, confidence scores, and betting recommendations powered by Google Gemini."
        keywords={['AFL predictions', 'AI betting tips', 'football predictions', 'sports betting AI', 'AFL AI analysis', 'betting predictions']}
        url="/predictions"
        structuredData={{
          "@context": "https://schema.org",
          "@type": "WebPage",
          "name": "AI Predictions",
          "description": "AI-generated AFL predictions and betting tips",
          "url": "https://footybets.ai/predictions",
          "mainEntity": {
            "@type": "ItemList",
            "name": "AFL Predictions",
            "description": "AI-generated predictions for AFL games"
          }
        }}
      />
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">AI Predictions</h1>
            <p className="text-gray-600">AI-generated AFL predictions and betting tips</p>
          </div>
          <div className="flex space-x-3">
            <button
              onClick={generatePredictions}
              disabled={generating}
              className="btn-primary flex items-center"
            >
              {generating ? (
                <div className="loading-spinner w-4 h-4 mr-2"></div>
              ) : (
                <PlayIcon className="w-4 h-4 mr-2" />
              )}
              {generating ? 'Generating...' : 'Generate Predictions'}
            </button>
            <button
              onClick={updateAccuracy}
              className="btn-secondary flex items-center"
            >
              <ArrowPathIcon className="w-4 h-4 mr-2" />
              Update Accuracy
            </button>
          </div>
        </div>

        {/* Predictions List */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Predictions</h2>
          {predictions.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Game
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Prediction
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Confidence
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Bet Recommendation
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Result
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {predictions.map((prediction) => (
                    <tr key={prediction.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {prediction.home_team_name} vs {prediction.away_team_name}
                          </div>
                          <div className="text-sm text-gray-500">
                            {prediction.predicted_home_score} - {prediction.predicted_away_score}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {prediction.predicted_winner_name}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`text-sm font-medium ${getConfidenceColor(prediction.confidence_score)}`}>
                          {(prediction.confidence_score * 100).toFixed(0)}%
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getBetRecommendationColor(prediction.recommended_bet)}`}>
                          {prediction.recommended_bet}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {format(new Date(prediction.prediction_date), 'MMM dd, yyyy')}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {prediction.is_correct !== null ? (
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            prediction.is_correct ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                          }`}>
                            {prediction.is_correct ? 'Correct' : 'Incorrect'}
                          </span>
                        ) : (
                          <span className="text-gray-400">Pending</span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <button
                          onClick={() => viewPredictionDetails(prediction)}
                          className="text-blue-600 hover:text-blue-900 flex items-center"
                        >
                          <EyeIcon className="w-4 h-4 mr-1" />
                          View
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-500 mb-4">No predictions available</p>
              <button
                onClick={generatePredictions}
                className="btn-primary"
              >
                Generate First Predictions
              </button>
            </div>
          )}
        </div>

        {/* Prediction Details Modal */}
        {showModal && selectedPrediction && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Prediction Details
                </h3>
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium text-gray-900">Game</h4>
                    <p className="text-gray-600">
                      {selectedPrediction.home_team_name} vs {selectedPrediction.away_team_name}
                    </p>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">Prediction</h4>
                    <p className="text-gray-600">
                      Winner: {selectedPrediction.predicted_winner_name}
                    </p>
                    <p className="text-gray-600">
                      Score: {selectedPrediction.predicted_home_score} - {selectedPrediction.predicted_away_score}
                    </p>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">Confidence</h4>
                    <p className={`${getConfidenceColor(selectedPrediction.confidence_score)}`}>
                      {(selectedPrediction.confidence_score * 100).toFixed(0)}%
                    </p>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">Bet Recommendation</h4>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getBetRecommendationColor(selectedPrediction.recommended_bet)}`}>
                      {selectedPrediction.recommended_bet}
                    </span>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">Reasoning</h4>
                    <p className="text-gray-600 text-sm">
                      {selectedPrediction.reasoning || 'No reasoning provided'}
                    </p>
                  </div>
                  {selectedPrediction.factors_considered && selectedPrediction.factors_considered.length > 0 && (
                    <div>
                      <h4 className="font-medium text-gray-900">Key Factors</h4>
                      <ul className="list-disc list-inside text-gray-600 text-sm">
                        {selectedPrediction.factors_considered.map((factor, index) => (
                          <li key={index}>{factor}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  <div>
                    <h4 className="font-medium text-gray-900">Model Version</h4>
                    <p className="text-gray-600">{selectedPrediction.model_version}</p>
                  </div>
                </div>
                <div className="mt-6 flex justify-end">
                  <button
                    onClick={() => setShowModal(false)}
                    className="btn-secondary"
                  >
                    Close
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default Predictions; 