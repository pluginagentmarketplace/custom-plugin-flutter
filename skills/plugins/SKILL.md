---
name: plugins
description: Flutter plugin development and native integration
sasmp_version: "2.0.0"
eqhm_version: "1.1.0"
bonded_agent: 08-flutter-platform-native
bond_type: PRIMARY_BOND
---

# Flutter Plugins Skill

## Overview
Develop Flutter plugins for native platform integration, including platform channels and federated plugin architecture. Master production-grade plugin development with 2024-2025 best practices.

## Topics Covered

### Platform Channels
- MethodChannel basics
- EventChannel for streams
- BasicMessageChannel
- Binary codecs
- Error handling

### Plugin Structure
- Plugin package anatomy
- Dart API design
- iOS implementation
- Android implementation
- Web support

### Federated Plugins
- Platform interface package
- Platform implementations
- Endorsed implementations
- Plugin composition
- Version coordination

### Native Features
- Camera integration
- File system access
- Sensor data
- Biometrics
- Background processing

### Publishing
- Plugin documentation
- pub.dev publishing
- Version management
- Change logging
- Maintenance

## Core Patterns

### 🔷 Plugin Package Structure

```
my_plugin/
├── lib/
│   ├── my_plugin.dart              # Public API
│   ├── src/
│   │   ├── my_plugin_method_channel.dart
│   │   └── my_plugin_platform_interface.dart
├── android/
│   ├── build.gradle
│   └── src/main/kotlin/.../MyPlugin.kt
├── ios/
│   ├── my_plugin.podspec
│   └── Classes/
│       └── MyPlugin.swift
├── example/
│   └── lib/main.dart
├── test/
│   └── my_plugin_test.dart
├── pubspec.yaml
├── CHANGELOG.md
└── README.md
```

### 🔶 Platform Interface Pattern

```dart
// lib/src/my_plugin_platform_interface.dart
import 'package:plugin_platform_interface/plugin_platform_interface.dart';
import 'my_plugin_method_channel.dart';

abstract class MyPluginPlatform extends PlatformInterface {
  MyPluginPlatform() : super(token: _token);

  static final Object _token = Object();

  static MyPluginPlatform _instance = MethodChannelMyPlugin();

  static MyPluginPlatform get instance => _instance;

  static set instance(MyPluginPlatform instance) {
    PlatformInterface.verifyToken(instance, _token);
    _instance = instance;
  }

  /// Returns the current battery level as a percentage (0-100)
  Future<int> getBatteryLevel() {
    throw UnimplementedError('getBatteryLevel() has not been implemented.');
  }

  /// Returns true if the device is currently charging
  Future<bool> isCharging() {
    throw UnimplementedError('isCharging() has not been implemented.');
  }

  /// Stream of battery level changes
  Stream<int> get batteryLevelStream {
    throw UnimplementedError('batteryLevelStream has not been implemented.');
  }
}
```

### 🟢 MethodChannel Implementation

```dart
// lib/src/my_plugin_method_channel.dart
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'my_plugin_platform_interface.dart';

class MethodChannelMyPlugin extends MyPluginPlatform {
  @visibleForTesting
  final methodChannel = const MethodChannel('com.example.my_plugin');

  @visibleForTesting
  final eventChannel = const EventChannel('com.example.my_plugin/events');

  @override
  Future<int> getBatteryLevel() async {
    try {
      final level = await methodChannel.invokeMethod<int>('getBatteryLevel');
      return level ?? 0;
    } on PlatformException catch (e) {
      throw BatteryException('Failed to get battery level: ${e.message}');
    }
  }

  @override
  Future<bool> isCharging() async {
    try {
      final charging = await methodChannel.invokeMethod<bool>('isCharging');
      return charging ?? false;
    } on PlatformException catch (e) {
      throw BatteryException('Failed to get charging status: ${e.message}');
    }
  }

  @override
  Stream<int> get batteryLevelStream {
    return eventChannel
        .receiveBroadcastStream()
        .map((event) => event as int)
        .handleError((error) {
      throw BatteryException('Battery stream error: $error');
    });
  }
}

class BatteryException implements Exception {
  final String message;
  BatteryException(this.message);

  @override
  String toString() => 'BatteryException: $message';
}
```

### 🟣 Public API

```dart
// lib/my_plugin.dart
import 'src/my_plugin_platform_interface.dart';

export 'src/my_plugin_platform_interface.dart' show BatteryException;

/// A Flutter plugin for accessing battery information
class MyPlugin {
  /// Returns the current battery level as a percentage (0-100)
  ///
  /// Throws [BatteryException] if the battery level cannot be retrieved
  ///
  /// Example:
  /// ```dart
  /// final level = await MyPlugin.getBatteryLevel();
  /// print('Battery: $level%');
  /// ```
  static Future<int> getBatteryLevel() {
    return MyPluginPlatform.instance.getBatteryLevel();
  }

  /// Returns true if the device is currently charging
  ///
  /// Throws [BatteryException] if the charging status cannot be determined
  static Future<bool> isCharging() {
    return MyPluginPlatform.instance.isCharging();
  }

  /// A stream that emits battery level changes
  ///
  /// The stream emits values from 0 to 100
  static Stream<int> get batteryLevelStream {
    return MyPluginPlatform.instance.batteryLevelStream;
  }
}
```

### 🔴 Android Implementation (Kotlin)

```kotlin
// android/src/main/kotlin/com/example/my_plugin/MyPlugin.kt
package com.example.my_plugin

import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.BatteryManager
import android.os.Build
import io.flutter.embedding.engine.plugins.FlutterPlugin
import io.flutter.plugin.common.EventChannel
import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel
import io.flutter.plugin.common.MethodChannel.MethodCallHandler
import io.flutter.plugin.common.MethodChannel.Result

class MyPlugin: FlutterPlugin, MethodCallHandler, EventChannel.StreamHandler {
    private lateinit var channel: MethodChannel
    private lateinit var eventChannel: EventChannel
    private lateinit var context: Context
    private var eventSink: EventChannel.EventSink? = null

    override fun onAttachedToEngine(binding: FlutterPlugin.FlutterPluginBinding) {
        context = binding.applicationContext

        channel = MethodChannel(binding.binaryMessenger, "com.example.my_plugin")
        channel.setMethodCallHandler(this)

        eventChannel = EventChannel(binding.binaryMessenger, "com.example.my_plugin/events")
        eventChannel.setStreamHandler(this)
    }

    override fun onMethodCall(call: MethodCall, result: Result) {
        when (call.method) {
            "getBatteryLevel" -> {
                val level = getBatteryLevel()
                if (level != -1) {
                    result.success(level)
                } else {
                    result.error("UNAVAILABLE", "Battery level not available", null)
                }
            }
            "isCharging" -> {
                result.success(isCharging())
            }
            else -> result.notImplemented()
        }
    }

    private fun getBatteryLevel(): Int {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            val batteryManager = context.getSystemService(Context.BATTERY_SERVICE) as BatteryManager
            batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
        } else {
            val intent = context.registerReceiver(null, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
            val level = intent?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) ?: -1
            val scale = intent?.getIntExtra(BatteryManager.EXTRA_SCALE, -1) ?: -1
            if (level >= 0 && scale > 0) (level * 100) / scale else -1
        }
    }

    private fun isCharging(): Boolean {
        val intent = context.registerReceiver(null, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
        val status = intent?.getIntExtra(BatteryManager.EXTRA_STATUS, -1) ?: -1
        return status == BatteryManager.BATTERY_STATUS_CHARGING ||
               status == BatteryManager.BATTERY_STATUS_FULL
    }

    // EventChannel StreamHandler
    override fun onListen(arguments: Any?, events: EventChannel.EventSink?) {
        eventSink = events
        // Start listening to battery changes and emit to eventSink
    }

    override fun onCancel(arguments: Any?) {
        eventSink = null
    }

    override fun onDetachedFromEngine(binding: FlutterPlugin.FlutterPluginBinding) {
        channel.setMethodCallHandler(null)
        eventChannel.setStreamHandler(null)
    }
}
```

### 🟠 iOS Implementation (Swift)

```swift
// ios/Classes/MyPlugin.swift
import Flutter
import UIKit

public class MyPlugin: NSObject, FlutterPlugin, FlutterStreamHandler {
    private var eventSink: FlutterEventSink?

    public static func register(with registrar: FlutterPluginRegistrar) {
        let channel = FlutterMethodChannel(
            name: "com.example.my_plugin",
            binaryMessenger: registrar.messenger()
        )
        let eventChannel = FlutterEventChannel(
            name: "com.example.my_plugin/events",
            binaryMessenger: registrar.messenger()
        )

        let instance = MyPlugin()
        registrar.addMethodCallDelegate(instance, channel: channel)
        eventChannel.setStreamHandler(instance)
    }

    public func handle(_ call: FlutterMethodCall, result: @escaping FlutterResult) {
        switch call.method {
        case "getBatteryLevel":
            result(getBatteryLevel())
        case "isCharging":
            result(isCharging())
        default:
            result(FlutterMethodNotImplemented)
        }
    }

    private func getBatteryLevel() -> Int {
        UIDevice.current.isBatteryMonitoringEnabled = true
        let level = UIDevice.current.batteryLevel

        if level < 0 {
            return -1 // Unknown
        }
        return Int(level * 100)
    }

    private func isCharging() -> Bool {
        UIDevice.current.isBatteryMonitoringEnabled = true
        let state = UIDevice.current.batteryState
        return state == .charging || state == .full
    }

    // FlutterStreamHandler
    public func onListen(
        withArguments arguments: Any?,
        eventSink events: @escaping FlutterEventSink
    ) -> FlutterError? {
        self.eventSink = events
        // Start observing battery level changes
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(batteryLevelDidChange),
            name: UIDevice.batteryLevelDidChangeNotification,
            object: nil
        )
        return nil
    }

    public func onCancel(withArguments arguments: Any?) -> FlutterError? {
        NotificationCenter.default.removeObserver(self)
        eventSink = nil
        return nil
    }

    @objc private func batteryLevelDidChange(_ notification: Notification) {
        eventSink?(getBatteryLevel())
    }
}
```

### 🔵 Federated Plugin Structure

```
my_plugin/
├── my_plugin/                          # App-facing package
│   ├── lib/my_plugin.dart
│   └── pubspec.yaml
│
├── my_plugin_platform_interface/       # Platform interface
│   ├── lib/
│   │   ├── my_plugin_platform_interface.dart
│   │   └── method_channel_my_plugin.dart
│   └── pubspec.yaml
│
├── my_plugin_android/                  # Android implementation
│   ├── android/
│   ├── lib/my_plugin_android.dart
│   └── pubspec.yaml
│
├── my_plugin_ios/                      # iOS implementation
│   ├── ios/
│   ├── lib/my_plugin_ios.dart
│   └── pubspec.yaml
│
├── my_plugin_web/                      # Web implementation
│   ├── lib/my_plugin_web.dart
│   └── pubspec.yaml
│
└── my_plugin_linux/                    # Linux implementation
    ├── linux/
    ├── lib/my_plugin_linux.dart
    └── pubspec.yaml
```

```yaml
# my_plugin/pubspec.yaml
name: my_plugin
version: 1.0.0

dependencies:
  flutter:
    sdk: flutter
  my_plugin_platform_interface: ^1.0.0

  # Endorsed implementations
  my_plugin_android: ^1.0.0
  my_plugin_ios: ^1.0.0
  my_plugin_web: ^1.0.0

flutter:
  plugin:
    platforms:
      android:
        default_package: my_plugin_android
      ios:
        default_package: my_plugin_ios
      web:
        default_package: my_plugin_web
```

## Plugin Testing

```dart
// test/my_plugin_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_plugin/my_plugin.dart';
import 'package:my_plugin/src/my_plugin_platform_interface.dart';
import 'package:mocktail/mocktail.dart';
import 'package:plugin_platform_interface/plugin_platform_interface.dart';

class MockMyPluginPlatform extends Mock
    with MockPlatformInterfaceMixin
    implements MyPluginPlatform {}

void main() {
  late MockMyPluginPlatform mockPlatform;

  setUp(() {
    mockPlatform = MockMyPluginPlatform();
    MyPluginPlatform.instance = mockPlatform;
  });

  group('MyPlugin', () {
    test('getBatteryLevel returns correct value', () async {
      when(() => mockPlatform.getBatteryLevel()).thenAnswer((_) async => 75);

      final result = await MyPlugin.getBatteryLevel();

      expect(result, 75);
      verify(() => mockPlatform.getBatteryLevel()).called(1);
    });

    test('isCharging returns correct value', () async {
      when(() => mockPlatform.isCharging()).thenAnswer((_) async => true);

      final result = await MyPlugin.isCharging();

      expect(result, isTrue);
    });

    test('getBatteryLevel throws BatteryException on error', () async {
      when(() => mockPlatform.getBatteryLevel())
          .thenThrow(BatteryException('Test error'));

      expect(
        () => MyPlugin.getBatteryLevel(),
        throwsA(isA<BatteryException>()),
      );
    });
  });
}
```

## Publishing Checklist

```markdown
## Pre-Publish Checklist

### Code Quality
- [ ] All tests passing
- [ ] No lint warnings (`flutter analyze`)
- [ ] Example app works on all platforms
- [ ] Error handling is comprehensive

### Documentation
- [ ] README.md with usage examples
- [ ] CHANGELOG.md updated
- [ ] API documentation complete
- [ ] Platform requirements documented

### pubspec.yaml
- [ ] Version number incremented
- [ ] Description is clear (<180 chars)
- [ ] Homepage URL is valid
- [ ] Issue tracker URL is valid
- [ ] Repository URL is valid
- [ ] Topics are relevant (max 5)

### Platform Specific
- [ ] Android minSdk specified
- [ ] iOS deployment target specified
- [ ] Permissions documented
- [ ] ProGuard rules if needed
```

```bash
# Publish commands
flutter pub publish --dry-run
flutter pub publish
```

## Troubleshooting Guide

### Common Issues

#### 1. MissingPluginException
```
❌ Error: MissingPluginException(No implementation found for method X)

✅ Solutions:
1. Hot restart instead of hot reload
2. Verify channel names match exactly
3. Check plugin registration in native code
4. Run `flutter clean && flutter pub get`
5. For iOS: `cd ios && pod install --repo-update`
```

#### 2. Build Failed - Android
```
❌ Error: Kotlin/Java compilation error

✅ Debug Checklist:
□ Check kotlin_version in android/build.gradle
□ Verify compileSdkVersion matches dependencies
□ Run ./gradlew clean in android/
□ Check for duplicate class definitions
```

#### 3. Build Failed - iOS
```
❌ Error: Swift/Objective-C compilation error

✅ Solutions:
1. Check podspec iOS deployment target
2. Run `pod repo update`
3. Delete Podfile.lock and pod install
4. Verify module imports are correct
```

#### 4. EventChannel Not Receiving Events
```
❌ Symptom: Stream returns nothing

✅ Debug Checklist:
□ Verify onListen is called (add print)
□ Check eventSink is not null before sending
□ Ensure native observation is started
□ Verify stream subscription is active
```

## Debug Commands

```bash
# Test plugin locally
cd example && flutter run

# Run plugin tests
flutter test

# Analyze code
flutter analyze

# Check pub score
pana

# Debug Android native
cd example/android && ./gradlew assembleDebug --info

# Debug iOS native
cd example/ios && xcodebuild -workspace Runner.xcworkspace -scheme Runner -configuration Debug
```

## Integration Points

| Agent | Integration |
|-------|-------------|
| 08-Platform-Native | Core plugin development |
| 06-Testing-QA | Plugin testing strategies |
| 07-DevOps | pub.dev publishing |

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Platform Coverage | ≥3 | Supported platforms |
| Test Coverage | ≥80% | Coverage report |
| Pub Score | ≥130 | pana analysis |
| Error Rate | <0.1% | Crashlytics |

## Prerequisites
- Flutter fundamentals
- iOS/Swift basics
- Android/Kotlin basics

## Learning Outcomes
- Create platform channels
- Build federated plugins
- Integrate native APIs
- Publish to pub.dev

## EQHM Compliance

- ✅ **Ethical**: Request only necessary permissions
- ✅ **Quality**: Comprehensive platform support
- ✅ **Honest**: Clear platform requirements
- ✅ **Maintainable**: Federated architecture

---

*This skill enables native platform integration through Flutter plugins.*
