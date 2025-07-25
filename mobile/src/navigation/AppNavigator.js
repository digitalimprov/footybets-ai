import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { Ionicons } from '@expo/vector-icons';

// Import screens
import DashboardScreen from '../screens/DashboardScreen';
import PredictionsScreen from '../screens/PredictionsScreen';
import GamesScreen from '../screens/GamesScreen';
import AnalyticsScreen from '../screens/AnalyticsScreen';
import ProfileScreen from '../screens/ProfileScreen';
import PredictionDetailScreen from '../screens/PredictionDetailScreen';
import GameDetailScreen from '../screens/GameDetailScreen';
import SettingsScreen from '../screens/SettingsScreen';
import NotificationsScreen from '../screens/NotificationsScreen';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

// Stack navigators for each tab
const DashboardStack = () => (
  <Stack.Navigator>
    <Stack.Screen 
      name="Dashboard" 
      component={DashboardScreen}
      options={{ headerShown: false }}
    />
  </Stack.Navigator>
);

const PredictionsStack = () => (
  <Stack.Navigator>
    <Stack.Screen 
      name="PredictionsList" 
      component={PredictionsScreen}
      options={{ title: 'AI Predictions' }}
    />
    <Stack.Screen 
      name="PredictionDetail" 
      component={PredictionDetailScreen}
      options={{ title: 'Prediction Details' }}
    />
  </Stack.Navigator>
);

const GamesStack = () => (
  <Stack.Navigator>
    <Stack.Screen 
      name="GamesList" 
      component={GamesScreen}
      options={{ title: 'AFL Games' }}
    />
    <Stack.Screen 
      name="GameDetail" 
      component={GameDetailScreen}
      options={{ title: 'Game Details' }}
    />
  </Stack.Navigator>
);

const AnalyticsStack = () => (
  <Stack.Navigator>
    <Stack.Screen 
      name="AnalyticsMain" 
      component={AnalyticsScreen}
      options={{ title: 'Analytics' }}
    />
  </Stack.Navigator>
);

const ProfileStack = () => (
  <Stack.Navigator>
    <Stack.Screen 
      name="ProfileMain" 
      component={ProfileScreen}
      options={{ title: 'Profile' }}
    />
    <Stack.Screen 
      name="Settings" 
      component={SettingsScreen}
      options={{ title: 'Settings' }}
    />
    <Stack.Screen 
      name="Notifications" 
      component={NotificationsScreen}
      options={{ title: 'Notifications' }}
    />
  </Stack.Navigator>
);

const AppNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          if (route.name === 'DashboardTab') {
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === 'PredictionsTab') {
            iconName = focused ? 'analytics' : 'analytics-outline';
          } else if (route.name === 'GamesTab') {
            iconName = focused ? 'calendar' : 'calendar-outline';
          } else if (route.name === 'AnalyticsTab') {
            iconName = focused ? 'bar-chart' : 'bar-chart-outline';
          } else if (route.name === 'ProfileTab') {
            iconName = focused ? 'person' : 'person-outline';
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#3b82f6',
        tabBarInactiveTintColor: 'gray',
        tabBarStyle: {
          paddingBottom: 5,
          paddingTop: 5,
          height: 60,
        },
        headerShown: false,
      })}
    >
      <Tab.Screen 
        name="DashboardTab" 
        component={DashboardStack}
        options={{ title: 'Dashboard' }}
      />
      <Tab.Screen 
        name="PredictionsTab" 
        component={PredictionsStack}
        options={{ title: 'Predictions' }}
      />
      <Tab.Screen 
        name="GamesTab" 
        component={GamesStack}
        options={{ title: 'Games' }}
      />
      <Tab.Screen 
        name="AnalyticsTab" 
        component={AnalyticsStack}
        options={{ title: 'Analytics' }}
      />
      <Tab.Screen 
        name="ProfileTab" 
        component={ProfileStack}
        options={{ title: 'Profile' }}
      />
    </Tab.Navigator>
  );
};

export default AppNavigator; 