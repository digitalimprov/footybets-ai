import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useSelector, useDispatch } from 'react-redux';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'react-native-linear-gradient';
import { format } from 'date-fns';

import { fetchPredictions } from '../store/slices/predictionsSlice';
import { fetchUpcomingGames } from '../store/slices/gamesSlice';
import { generatePredictions } from '../store/slices/predictionsSlice';
import { apiService } from '../services/apiService';
import StatCard from '../components/StatCard';
import PredictionCard from '../components/PredictionCard';
import GameCard from '../components/GameCard';
import LoadingSpinner from '../components/LoadingSpinner';

const DashboardScreen = () => {
  const dispatch = useDispatch();
  const [refreshing, setRefreshing] = useState(false);
  const [stats, setStats] = useState({
    totalPredictions: 0,
    accuracy: 0,
    upcomingGames: 0,
    totalGames: 0,
  });

  const { predictions, loading, generating } = useSelector((state) => state.predictions);
  const { upcomingGames } = useSelector((state) => state.games);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      await Promise.all([
        dispatch(fetchPredictions()),
        dispatch(fetchUpcomingGames(7)),
        loadStats(),
      ]);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    }
  };

  const loadStats = async () => {
    try {
      const analytics = await apiService.getAnalyticsOverview('all');
      setStats({
        totalPredictions: analytics.total_predictions || 0,
        accuracy: analytics.accuracy_percentage || 0,
        upcomingGames: upcomingGames?.length || 0,
        totalGames: analytics.total_games || 0,
      });
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadDashboardData();
    setRefreshing(false);
  };

  const handleGeneratePredictions = async () => {
    Alert.alert(
      'Generate Predictions',
      'This will generate new AI predictions for upcoming games. Continue?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Generate',
          onPress: async () => {
            try {
              await dispatch(generatePredictions(7));
              Alert.alert('Success', 'New predictions generated successfully!');
            } catch (error) {
              Alert.alert('Error', 'Failed to generate predictions. Please try again.');
            }
          },
        },
      ]
    );
  };

  const recentPredictions = predictions.slice(0, 3);
  const nextGames = upcomingGames?.slice(0, 3) || [];

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>FootyBets.ai</Text>
          <Text style={styles.subtitle}>AI AFL Predictions</Text>
        </View>

        {/* Stats Grid */}
        <View style={styles.statsGrid}>
          <StatCard
            title="Total Predictions"
            value={stats.totalPredictions}
            icon="analytics"
            color="#3b82f6"
          />
          <StatCard
            title="Accuracy"
            value={`${stats.accuracy.toFixed(1)}%`}
            icon="checkmark-circle"
            color="#10b981"
          />
          <StatCard
            title="Upcoming Games"
            value={stats.upcomingGames}
            icon="calendar"
            color="#f59e0b"
          />
          <StatCard
            title="Total Games"
            value={stats.totalGames}
            icon="football"
            color="#8b5cf6"
          />
        </View>

        {/* Quick Actions */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Quick Actions</Text>
          <View style={styles.actionButtons}>
            <TouchableOpacity
              style={styles.actionButton}
              onPress={handleGeneratePredictions}
              disabled={generating}
            >
              <LinearGradient
                colors={['#3b82f6', '#1d4ed8']}
                style={styles.actionGradient}
              >
                <Ionicons name="refresh" size={24} color="white" />
                <Text style={styles.actionText}>
                  {generating ? 'Generating...' : 'Generate Predictions'}
                </Text>
              </LinearGradient>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.actionButton}
              onPress={() => {
                // Navigate to predictions screen
              }}
            >
              <LinearGradient
                colors={['#10b981', '#059669']}
                style={styles.actionGradient}
              >
                <Ionicons name="eye" size={24} color="white" />
                <Text style={styles.actionText}>View All Predictions</Text>
              </LinearGradient>
            </TouchableOpacity>
          </View>
        </View>

        {/* Recent Predictions */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Recent Predictions</Text>
          {recentPredictions.length > 0 ? (
            recentPredictions.map((prediction) => (
              <PredictionCard key={prediction.id} prediction={prediction} />
            ))
          ) : (
            <View style={styles.emptyState}>
              <Ionicons name="analytics-outline" size={48} color="#9ca3af" />
              <Text style={styles.emptyText}>No predictions yet</Text>
              <Text style={styles.emptySubtext}>
                Generate your first predictions to get started
              </Text>
            </View>
          )}
        </View>

        {/* Upcoming Games */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Upcoming Games</Text>
          {nextGames.length > 0 ? (
            nextGames.map((game) => (
              <GameCard key={game.id} game={game} />
            ))
          ) : (
            <View style={styles.emptyState}>
              <Ionicons name="calendar-outline" size={48} color="#9ca3af" />
              <Text style={styles.emptyText}>No upcoming games</Text>
              <Text style={styles.emptySubtext}>
                Check back later for new games
              </Text>
            </View>
          )}
        </View>

        {/* Last Updated */}
        <View style={styles.footer}>
          <Text style={styles.footerText}>
            Last updated: {format(new Date(), 'MMM dd, yyyy HH:mm')}
          </Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  scrollView: {
    flex: 1,
  },
  header: {
    padding: 20,
    backgroundColor: '#3b82f6',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: 'white',
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: '#dbeafe',
    textAlign: 'center',
    marginTop: 4,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 16,
    gap: 12,
  },
  section: {
    padding: 16,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 16,
  },
  actionButtons: {
    gap: 12,
  },
  actionButton: {
    borderRadius: 12,
    overflow: 'hidden',
  },
  actionGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    gap: 8,
  },
  actionText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  emptyState: {
    alignItems: 'center',
    padding: 32,
    backgroundColor: 'white',
    borderRadius: 12,
    marginTop: 8,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#6b7280',
    marginTop: 12,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#9ca3af',
    textAlign: 'center',
    marginTop: 4,
  },
  footer: {
    padding: 16,
    alignItems: 'center',
  },
  footerText: {
    fontSize: 12,
    color: '#9ca3af',
  },
});

export default DashboardScreen; 