import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import { Platform } from 'react-native';
import { apiService } from './apiService';

// Configure notification behavior
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: false,
  }),
});

export const setupNotifications = async () => {
  try {
    // Check if device supports notifications
    if (!Device.isDevice) {
      console.log('Must use physical device for Push Notifications');
      return;
    }

    // Request permissions
    const { status: existingStatus } = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;

    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }

    if (finalStatus !== 'granted') {
      console.log('Failed to get push token for push notification!');
      return;
    }

    // Get push token
    const token = await Notifications.getExpoPushTokenAsync({
      projectId: process.env.EXPO_PUBLIC_PROJECT_ID,
    });

    // Register token with backend
    if (token.data) {
      await apiService.registerForPushNotifications(token.data);
    }

    // Platform-specific setup
    if (Platform.OS === 'android') {
      Notifications.setNotificationChannelAsync('default', {
        name: 'default',
        importance: Notifications.AndroidImportance.MAX,
        vibrationPattern: [0, 250, 250, 250],
        lightColor: '#FF231F7C',
      });
    }

    return token;
  } catch (error) {
    console.error('Error setting up notifications:', error);
  }
};

export const scheduleLocalNotification = async ({
  title,
  body,
  data = {},
  trigger = null,
}) => {
  try {
    await Notifications.scheduleNotificationAsync({
      content: {
        title,
        body,
        data,
      },
      trigger,
    });
  } catch (error) {
    console.error('Error scheduling notification:', error);
  }
};

export const cancelAllNotifications = async () => {
  try {
    await Notifications.cancelAllScheduledNotificationsAsync();
  } catch (error) {
    console.error('Error canceling notifications:', error);
  }
};

export const getNotificationSettings = async () => {
  try {
    const settings = await Notifications.getPermissionsAsync();
    return settings;
  } catch (error) {
    console.error('Error getting notification settings:', error);
    return null;
  }
};

export const updateNotificationSettings = async (settings) => {
  try {
    await apiService.updateNotificationSettings(settings);
  } catch (error) {
    console.error('Error updating notification settings:', error);
  }
};

// Notification categories for different types of notifications
export const setupNotificationCategories = async () => {
  await Notifications.setNotificationCategoryAsync('prediction', [
    {
      identifier: 'view_prediction',
      buttonTitle: 'View Prediction',
      options: {
        isDestructive: false,
        isAuthenticationRequired: false,
      },
    },
    {
      identifier: 'dismiss',
      buttonTitle: 'Dismiss',
      options: {
        isDestructive: true,
        isAuthenticationRequired: false,
      },
    },
  ]);

  await Notifications.setNotificationCategoryAsync('game_result', [
    {
      identifier: 'view_result',
      buttonTitle: 'View Result',
      options: {
        isDestructive: false,
        isAuthenticationRequired: false,
      },
    },
  ]);
};

// Handle notification responses
export const handleNotificationResponse = (response) => {
  const { actionIdentifier, notification } = response;
  
  switch (actionIdentifier) {
    case 'view_prediction':
      // Navigate to prediction detail
      console.log('Navigate to prediction:', notification.request.content.data.predictionId);
      break;
    case 'view_result':
      // Navigate to game result
      console.log('Navigate to game result:', notification.request.content.data.gameId);
      break;
    case 'dismiss':
      // Dismiss notification
      break;
    default:
      // Handle default tap
      console.log('Notification tapped:', notification.request.content.data);
  }
}; 