# FootyBets.ai Mobile App Setup Guide

This guide will help you set up and run the FootyBets.ai mobile application for both iOS and Android platforms.

## 🚀 Quick Start

### Prerequisites

- **Node.js 18+** and npm
- **Expo CLI**: `npm install -g @expo/cli`
- **iOS Development**: Xcode (for iOS simulator and builds)
- **Android Development**: Android Studio (for Android emulator and builds)
- **Physical Device**: For testing push notifications and biometric features

### Installation

1. **Navigate to mobile directory**
   ```bash
   cd mobile
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Start development server**
   ```bash
   npx expo start
   ```

## 📱 Running the App

### Development Options

1. **iOS Simulator** (macOS only)
   - Press `i` in the terminal
   - Or scan QR code with Camera app

2. **Android Emulator**
   - Press `a` in the terminal
   - Or scan QR code with Expo Go app

3. **Physical Device**
   - Install Expo Go from App Store/Google Play
   - Scan QR code with Expo Go app

### Platform-Specific Setup

#### iOS Development

1. **Install Xcode** from Mac App Store
2. **Install iOS Simulator** through Xcode
3. **Set up certificates** for device testing:
   ```bash
   npx expo run:ios --device
   ```

#### Android Development

1. **Install Android Studio**
2. **Set up Android SDK** and emulator
3. **Configure environment variables**:
   ```bash
   export ANDROID_HOME=$HOME/Library/Android/sdk
   export PATH=$PATH:$ANDROID_HOME/emulator
   export PATH=$PATH:$ANDROID_HOME/tools
   export PATH=$PATH:$ANDROID_HOME/tools/bin
   export PATH=$PATH:$ANDROID_HOME/platform-tools
   ```

## 🏗️ Building for Production

### Using EAS Build (Recommended)

1. **Install EAS CLI**
   ```bash
   npm install -g @expo/eas-cli
   ```

2. **Login to Expo**
   ```bash
   eas login
   ```

3. **Configure EAS**
   ```bash
   eas build:configure
   ```

4. **Build for platforms**

   **iOS:**
   ```bash
   eas build --platform ios
   ```

   **Android:**
   ```bash
   eas build --platform android
   ```

   **Both:**
   ```bash
   eas build --platform all
   ```

### Manual Build (Advanced)

#### iOS Build
```bash
npx expo run:ios --configuration Release
```

#### Android Build
```bash
npx expo run:android --variant release
```

## 📦 App Store Deployment

### iOS App Store

1. **Create App Store Connect record**
2. **Upload build**:
   ```bash
   eas submit --platform ios
   ```
3. **Submit for review** through App Store Connect

### Google Play Store

1. **Create Google Play Console record**
2. **Upload APK/AAB**:
   ```bash
   eas submit --platform android
   ```
3. **Submit for review** through Google Play Console

## 🔧 Configuration

### Environment Variables

Update your `.env` file with:

```env
# API Configuration
EXPO_PUBLIC_API_URL=https://your-backend-url.com
EXPO_PUBLIC_APP_NAME=FootyBets.ai
EXPO_PUBLIC_VERSION=1.0.0

# Expo Configuration
EXPO_PUBLIC_PROJECT_ID=your-expo-project-id

# Push Notifications
EXPO_PUBLIC_PUSH_TOKEN=your-push-token

# Feature Flags
EXPO_PUBLIC_ENABLE_BIOMETRICS=true
EXPO_PUBLIC_ENABLE_PUSH_NOTIFICATIONS=true
```

### App Configuration

Update `app.json` with your app details:

```json
{
  "expo": {
    "name": "FootyBets.ai",
    "slug": "footybets-mobile",
    "version": "1.0.0",
    "ios": {
      "bundleIdentifier": "com.yourcompany.footybets",
      "buildNumber": "1.0.0"
    },
    "android": {
      "package": "com.yourcompany.footybets",
      "versionCode": 1
    }
  }
}
```

## 🔐 Security Features

### Biometric Authentication

The app supports Face ID (iOS) and Fingerprint (Android):

1. **Enable in settings**:
   ```javascript
   await storageService.setBiometricEnabled(true);
   ```

2. **Configure permissions** in `app.json`

### Secure Storage

- **Auth tokens** stored in SecureStore
- **User preferences** in AsyncStorage
- **Offline data** with encryption

## 📊 Analytics & Monitoring

### Crash Reporting

1. **Install Sentry** (optional):
   ```bash
   npx expo install @sentry/react-native
   ```

2. **Configure in App.js**:
   ```javascript
   import * as Sentry from '@sentry/react-native';
   Sentry.init({
     dsn: 'your-sentry-dsn',
   });
   ```

### Performance Monitoring

- **Expo Performance** built-in
- **Custom metrics** via API calls
- **User behavior** tracking

## 🔄 Updates & Maintenance

### Over-the-Air Updates

1. **Publish updates**:
   ```bash
   npx expo publish
   ```

2. **Configure update policy** in `app.json`

### Version Management

- **Semantic versioning** for releases
- **Automatic updates** for minor versions
- **Manual updates** for major versions

## 🧪 Testing

### Unit Tests
```bash
npm test
```

### E2E Tests
```bash
npm run test:e2e
```

### Manual Testing Checklist

- [ ] App launches successfully
- [ ] Navigation works on all screens
- [ ] API calls function properly
- [ ] Offline mode works
- [ ] Push notifications received
- [ ] Biometric authentication works
- [ ] Dark mode toggle works
- [ ] Data persistence works

## 🐛 Troubleshooting

### Common Issues

1. **Metro bundler issues**:
   ```bash
   npx expo start --clear
   ```

2. **iOS build failures**:
   ```bash
   cd ios && pod install && cd ..
   ```

3. **Android build failures**:
   ```bash
   npx expo run:android --clear
   ```

4. **Push notification issues**:
   - Check device permissions
   - Verify Expo push token
   - Test on physical device

### Debug Mode

Enable debug mode in `.env`:
```env
EXPO_PUBLIC_DEBUG_MODE=true
```

## 📚 Additional Resources

- [Expo Documentation](https://docs.expo.dev/)
- [React Native Documentation](https://reactnative.dev/)
- [EAS Build Documentation](https://docs.expo.dev/build/introduction/)
- [Expo Notifications](https://docs.expo.dev/versions/latest/sdk/notifications/)

## 🤝 Support

For issues and questions:
1. Check the troubleshooting section
2. Review Expo documentation
3. Search existing GitHub issues
4. Create a new issue with detailed information

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 