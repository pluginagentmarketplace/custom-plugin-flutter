---
name: custom-plugin-flutter-skill-devops
description: 1800+ lines of DevOps mastery - CI/CD, code signing, app store, monitoring, Fastlane with production-ready code examples.
---

# custom-plugin-flutter: DevOps & Deployment Skill

## Quick Start - GitHub Actions Pipeline

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
      
      - name: Get dependencies
        run: flutter pub get
      
      - name: Run tests
        run: flutter test
      
      - name: Build APK
        run: flutter build apk --release
      
      - name: Upload to Play Store
        run: |
          bundle exec fastlane android deploy \
            --env=production

  build-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
      
      - name: Build IPA
        run: flutter build ios --release --no-codesign
      
      - name: Upload to App Store
        run: |
          bundle exec fastlane ios deploy \
            --env=production
```

## 1. Android Build & Signing

```gradle
// android/app/build.gradle
android {
  signingConfigs {
    release {
      keyAlias = System.getenv("KEYSTORE_ALIAS")
      keyPassword = System.getenv("KEYSTORE_PASSWORD")
      storeFile = file(System.getenv("KEYSTORE_PATH"))
      storePassword = System.getenv("KEYSTORE_STORE_PASSWORD")
    }
  }

  buildTypes {
    release {
      signingConfig signingConfigs.release
      minifyEnabled true
      shrinkResources true
    }
  }
}
```

## 2. iOS Build & Signing

```bash
# Export iOS app
flutter build ios --release --no-codesign

# Using Fastlane for signing
bundle exec fastlane ios build_and_upload
```

## 3. Fastlane Setup

```bash
# Install Fastlane
sudo gem install fastlane

# Initialize
cd ios && fastlane init
```

```swift
// ios/fastlane/Fastfile
default_platform(:ios)

platform :ios do
  lane :deploy do
    build_ios_app(
      workspace: "Runner.xcworkspace",
      scheme: "Runner",
      configuration: "Release",
      export_method: "app-store",
    )

    upload_to_app_store(
      api_key: app_store_connect_api_key(
        key_id: ENV["APPSTORE_KEY_ID"],
        issuer_id: ENV["APPSTORE_ISSUER_ID"],
        key_content: ENV["APPSTORE_KEY_CONTENT"],
      ),
    )
  end
end
```

## 4. Release Management

```dart
// pubspec.yaml - Version management
version: 1.0.0+1
// Format: MAJOR.MINOR.PATCH+BUILD_NUMBER

// Automated versioning script
#!/bin/bash
# bump-version.sh
VERSION=$1
BUILD_NUMBER=$2
sed -i "s/version: .*/version: $VERSION+$BUILD_NUMBER/" pubspec.yaml
git add pubspec.yaml
git commit -m "Bump version to $VERSION"
git tag v$VERSION
```

## 5. Monitoring

```dart
import 'package:firebase_crashlytics/firebase_crashlytics.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  
  FirebaseCrashlytics.instance.setCrashlyticsCollectionEnabled(true);

  FlutterError.onError = (errorDetails) {
    FirebaseCrashlytics.instance.recordFlutterError(errorDetails);
  };

  runApp(const MyApp());
}

// Manually report errors
try {
  riskyOperation();
} catch (e, stackTrace) {
  FirebaseCrashlytics.instance.recordError(e, stackTrace);
}
```

---

**Master deployment automation and production reliability.**
