import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { format } from 'date-fns';

const PredictionCard = ({ prediction, onPress }) => {
  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return '#10b981';
    if (confidence >= 0.6) return '#f59e0b';
    return '#ef4444';
  };

  const getConfidenceText = (confidence) => {
    if (confidence >= 0.8) return 'High';
    if (confidence >= 0.6) return 'Medium';
    return 'Low';
  };

  const getBetRecommendationColor = (recommendation) => {
    switch (recommendation?.toLowerCase()) {
      case 'home':
        return '#3b82f6';
      case 'away':
        return '#8b5cf6';
      case 'draw':
        return '#f59e0b';
      default:
        return '#6b7280';
    }
  };

  return (
    <TouchableOpacity style={styles.container} onPress={onPress}>
      <View style={styles.header}>
        <View style={styles.teams}>
          <Text style={styles.teamText}>
            {prediction.home_team_name} vs {prediction.away_team_name}
          </Text>
          <Text style={styles.dateText}>
            {format(new Date(prediction.game_date), 'MMM dd, yyyy')}
          </Text>
        </View>
        <View style={styles.predictionBadge}>
          <Text style={styles.predictionText}>
            {prediction.predicted_winner_name}
          </Text>
        </View>
      </View>

      <View style={styles.details}>
        <View style={styles.scorePrediction}>
          <Text style={styles.scoreText}>
            {prediction.predicted_home_score} - {prediction.predicted_away_score}
          </Text>
          <Text style={styles.scoreLabel}>Predicted Score</Text>
        </View>

        <View style={styles.confidenceSection}>
          <View style={styles.confidenceItem}>
            <Text style={styles.confidenceLabel}>Confidence</Text>
            <View style={styles.confidenceValue}>
              <Text
                style={[
                  styles.confidenceText,
                  { color: getConfidenceColor(prediction.confidence_score) },
                ]}
              >
                {getConfidenceText(prediction.confidence_score)}
              </Text>
              <Text style={styles.confidencePercentage}>
                {(prediction.confidence_score * 100).toFixed(0)}%
              </Text>
            </View>
          </View>

          {prediction.recommended_bet && (
            <View style={styles.betRecommendation}>
              <Text style={styles.betLabel}>Bet Recommendation</Text>
              <View
                style={[
                  styles.betBadge,
                  { backgroundColor: getBetRecommendationColor(prediction.recommended_bet) },
                ]}
              >
                <Text style={styles.betText}>
                  {prediction.recommended_bet.toUpperCase()}
                </Text>
              </View>
            </View>
          )}
        </View>

        {prediction.is_correct !== null && (
          <View style={styles.resultSection}>
            <Ionicons
              name={prediction.is_correct ? 'checkmark-circle' : 'close-circle'}
              size={20}
              color={prediction.is_correct ? '#10b981' : '#ef4444'}
            />
            <Text
              style={[
                styles.resultText,
                { color: prediction.is_correct ? '#10b981' : '#ef4444' },
              ]}
            >
              {prediction.is_correct ? 'Correct' : 'Incorrect'}
            </Text>
          </View>
        )}
      </View>

      <View style={styles.footer}>
        <Text style={styles.modelText}>
          Model: {prediction.model_version}
        </Text>
        <Text style={styles.dateText}>
          {format(new Date(prediction.prediction_date), 'MMM dd, HH:mm')}
        </Text>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  teams: {
    flex: 1,
  },
  teamText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: 4,
  },
  dateText: {
    fontSize: 12,
    color: '#6b7280',
  },
  predictionBadge: {
    backgroundColor: '#3b82f6',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  predictionText: {
    color: 'white',
    fontSize: 12,
    fontWeight: '600',
  },
  details: {
    marginBottom: 12,
  },
  scorePrediction: {
    alignItems: 'center',
    marginBottom: 12,
  },
  scoreText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1f2937',
  },
  scoreLabel: {
    fontSize: 12,
    color: '#6b7280',
    marginTop: 2,
  },
  confidenceSection: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  confidenceItem: {
    alignItems: 'center',
  },
  confidenceLabel: {
    fontSize: 12,
    color: '#6b7280',
    marginBottom: 4,
  },
  confidenceValue: {
    alignItems: 'center',
  },
  confidenceText: {
    fontSize: 14,
    fontWeight: '600',
  },
  confidencePercentage: {
    fontSize: 12,
    color: '#6b7280',
  },
  betRecommendation: {
    alignItems: 'center',
  },
  betLabel: {
    fontSize: 12,
    color: '#6b7280',
    marginBottom: 4,
  },
  betBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  betText: {
    color: 'white',
    fontSize: 12,
    fontWeight: '600',
  },
  resultSection: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 8,
    gap: 4,
  },
  resultText: {
    fontSize: 14,
    fontWeight: '600',
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#f3f4f6',
  },
  modelText: {
    fontSize: 12,
    color: '#6b7280',
  },
});

export default PredictionCard; 