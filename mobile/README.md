# FootyBets.ai Mobile App

React Native mobile application for iOS and Android platforms that connects to the FootyBets.ai backend API.

## Features

- **Cross-platform**: Single codebase for iOS and Android
- **Real-time updates**: Live prediction updates and notifications
- **Offline support**: Cache predictions and data for offline viewing
- **Push notifications**: Get notified of new predictions and game results
- **Native performance**: Optimized for mobile devices
- **Dark mode support**: Automatic theme switching
- **Biometric authentication**: Secure login with Face ID/Touch ID

## Tech Stack

- **Framework**: React Native with Expo
- **Navigation**: React Navigation v6
- **State Management**: Redux Toolkit
- **UI Components**: React Native Elements + Custom components
- **Charts**: React Native Chart Kit
- **Notifications**: Expo Notifications
- **Storage**: AsyncStorage + SQLite
- **Networking**: Axios with interceptors
- **Authentication**: Expo SecureStore

## Project Structure

```
mobile/
├── src/
│   ├── components/          # Reusable UI components
│   ├── screens/            # Screen components
│   ├── navigation/         # Navigation configuration
│   ├── store/             # Redux store and slices
│   ├── services/          # API services
│   ├── utils/             # Utility functions
│   ├── hooks/             # Custom React hooks
│   ├── constants/         # App constants
│   └── assets/            # Images, fonts, etc.
├── android/               # Android-specific files
├── ios/                   # iOS-specific files
├── app.json              # Expo configuration
├── package.json          # Dependencies
└── README.md             # This file
```

## Quick Start

### Prerequisites

- Node.js 18+
- Expo CLI
- iOS Simulator (for iOS development)
- Android Studio (for Android development)

### Installation

1. **Install Expo CLI**
   ```bash
   npm install -g @expo/cli
   ```

2. **Install dependencies**
   ```bash
   cd mobile
   npm install
   ```

3. **Start development server**
   ```bash
   npx expo start
   ```

4. **Run on device/simulator**
   - Press `i` for iOS simulator
   - Press `a` for Android emulator
   - Scan QR code with Expo Go app on physical device

## Development

### Environment Setup

Create a `.env` file in the mobile directory:

```env
EXPO_PUBLIC_API_URL=http://localhost:8000
EXPO_PUBLIC_APP_NAME=FootyBets.ai
EXPO_PUBLIC_VERSION=1.0.0
```

### Building for Production

**iOS:**
```bash
npx expo build:ios
```

**Android:**
```bash
npx expo build:android
```

### Publishing Updates

```bash
npx expo publish
```

## API Integration

The mobile app connects to the same backend API as the web application:

- **Base URL**: Configurable via environment variables
- **Authentication**: JWT tokens stored securely
- **Real-time**: WebSocket connections for live updates
- **Offline**: Local storage for cached data

## Platform-Specific Features

### iOS
- Face ID/Touch ID authentication
- Apple Push Notifications
- iOS-specific UI components
- Background app refresh

### Android
- Fingerprint authentication
- Firebase Cloud Messaging
- Material Design components
- Background services

## Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e
```

## Deployment

### App Store (iOS)
1. Build production app
2. Upload to App Store Connect
3. Submit for review

### Google Play Store (Android)
1. Build production APK/AAB
2. Upload to Google Play Console
3. Submit for review

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details 