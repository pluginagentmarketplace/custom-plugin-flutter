---
name: custom-plugin-flutter-skill-plugins
description: Production-grade Flutter plugin development mastery - Platform channels, federated architecture, MethodChannel/EventChannel, iOS Swift/Android Kotlin integration, pub.dev publishing with comprehensive code examples
sasmp_version: "1.3.0"
bonded_agent: 08-flutter-platform-native
bond_type: PRIMARY_BOND
---

# custom-plugin-flutter: Plugins Skill

## Quick Start - Create Production Plugin

```bash
# Create federated plugin
flutter create --template=plugin --platforms=android,ios,web my_plugin

# Plugin structure
my_plugin/
├── lib/
│   ├── my_plugin.dart              # Public API
│   └── my_plugin_method_channel.dart
├── android/
│   └── src/main/kotlin/.../MyPlugin.kt
├── ios/
│   └── Classes/MyPlugin.swift
├── example/                         # Example app
├── test/                           # Unit tests
├── pubspec.yaml
└── README.md
```

```dart
// lib/my_plugin.dart - Public API
import 'my_plugin_platform_interface.dart';

class MyPlugin {
  Future<String?> getPlatformVersion() {
    return MyPluginPlatform.instance.getPlatformVersion();
  }

  Future<void> initialize({required String apiKey}) {
    return MyPluginPlatform.instance.initialize(apiKey: apiKey);
  }

  Stream<SensorData> get sensorStream {
    return MyPluginPlatform.instance.sensorStream;
  }
}
```

## 1. MethodChannel (Request/Response)

### Dart Implementation

```dart
class MethodChannelMyPlugin extends MyPluginPlatform {
  static const _channel = MethodChannel('com.example/my_plugin');

  @override
  Future<String?> getPlatformVersion() async {
    try {
      return await _channel.invokeMethod<String>('getPlatformVersion');
    } on PlatformException catch (e) {
      throw PluginException('Failed to get version: ${e.message}');
    }
  }

  @override
  Future<Map<String, dynamic>> getDeviceInfo() async {
    try {
      final result = await _channel.invokeMethod<Map>('getDeviceInfo');
      return Map<String, dynamic>.from(result ?? {});
    } on PlatformException catch (e) {
      throw PluginException('Failed to get device info: ${e.message}');
    }
  }

  @override
  Future<void> performAction(ActionParams params) async {
    try {
      await _channel.invokeMethod('performAction', params.toMap());
    } on PlatformException catch (e) {
      throw PluginException('Action failed: ${e.message}');
    }
  }
}
```

### iOS Swift Implementation

```swift
// ios/Classes/MyPlugin.swift
import Flutter
import UIKit

public class MyPlugin: NSObject, FlutterPlugin {
  public static func register(with registrar: FlutterPluginRegistrar) {
    let channel = FlutterMethodChannel(
      name: "com.example/my_plugin",
      binaryMessenger: registrar.messenger()
    )
    let instance = MyPlugin()
    registrar.addMethodCallDelegate(instance, channel: channel)
  }

  public func handle(_ call: FlutterMethodCall, result: @escaping FlutterResult) {
    switch call.method {
    case "getPlatformVersion":
      result("iOS " + UIDevice.current.systemVersion)

    case "getDeviceInfo":
      result([
        "model": UIDevice.current.model,
        "name": UIDevice.current.name,
        "systemVersion": UIDevice.current.systemVersion
      ])

    case "performAction":
      guard let args = call.arguments as? [String: Any] else {
        result(FlutterError(code: "INVALID_ARGS", message: "Invalid arguments", details: nil))
        return
      }
      // Perform action with args
      result(nil)

    default:
      result(FlutterMethodNotImplemented)
    }
  }
}
```

### Android Kotlin Implementation

```kotlin
// android/src/main/kotlin/.../MyPlugin.kt
package com.example.my_plugin

import io.flutter.embedding.engine.plugins.FlutterPlugin
import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel
import io.flutter.plugin.common.MethodChannel.MethodCallHandler
import io.flutter.plugin.common.MethodChannel.Result

class MyPlugin: FlutterPlugin, MethodCallHandler {
  private lateinit var channel: MethodChannel

  override fun onAttachedToEngine(binding: FlutterPlugin.FlutterPluginBinding) {
    channel = MethodChannel(binding.binaryMessenger, "com.example/my_plugin")
    channel.setMethodCallHandler(this)
  }

  override fun onMethodCall(call: MethodCall, result: Result) {
    when (call.method) {
      "getPlatformVersion" -> {
        result.success("Android ${android.os.Build.VERSION.RELEASE}")
      }
      "getDeviceInfo" -> {
        result.success(mapOf(
          "model" to android.os.Build.MODEL,
          "manufacturer" to android.os.Build.MANUFACTURER,
          "version" to android.os.Build.VERSION.RELEASE
        ))
      }
      "performAction" -> {
        val args = call.arguments as? Map<*, *>
        // Perform action
        result.success(null)
      }
      else -> result.notImplemented()
    }
  }

  override fun onDetachedFromEngine(binding: FlutterPlugin.FlutterPluginBinding) {
    channel.setMethodCallHandler(null)
  }
}
```

## 2. EventChannel (Streams)

### Dart Implementation

```dart
class MethodChannelMyPlugin extends MyPluginPlatform {
  static const _eventChannel = EventChannel('com.example/my_plugin/events');

  Stream<SensorData>? _sensorStream;

  @override
  Stream<SensorData> get sensorStream {
    _sensorStream ??= _eventChannel
        .receiveBroadcastStream()
        .map((event) => SensorData.fromMap(event as Map));
    return _sensorStream!;
  }
}

class SensorData {
  final double x, y, z;
  final DateTime timestamp;

  SensorData({required this.x, required this.y, required this.z, required this.timestamp});

  factory SensorData.fromMap(Map map) {
    return SensorData(
      x: map['x'] as double,
      y: map['y'] as double,
      z: map['z'] as double,
      timestamp: DateTime.fromMillisecondsSinceEpoch(map['timestamp'] as int),
    );
  }
}
```

### iOS EventChannel

```swift
class SensorStreamHandler: NSObject, FlutterStreamHandler {
  private var eventSink: FlutterEventSink?
  private var timer: Timer?

  func onListen(withArguments arguments: Any?, eventSink events: @escaping FlutterEventSink) -> FlutterError? {
    self.eventSink = events
    startSensorUpdates()
    return nil
  }

  func onCancel(withArguments arguments: Any?) -> FlutterError? {
    stopSensorUpdates()
    eventSink = nil
    return nil
  }

  private func startSensorUpdates() {
    timer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { [weak self] _ in
      self?.eventSink?([
        "x": 1.0,
        "y": 2.0,
        "z": 3.0,
        "timestamp": Int(Date().timeIntervalSince1970 * 1000)
      ])
    }
  }

  private func stopSensorUpdates() {
    timer?.invalidate()
    timer = nil
  }
}

// Register in plugin
public static func register(with registrar: FlutterPluginRegistrar) {
  let eventChannel = FlutterEventChannel(
    name: "com.example/my_plugin/events",
    binaryMessenger: registrar.messenger()
  )
  eventChannel.setStreamHandler(SensorStreamHandler())
}
```

### Android EventChannel

```kotlin
class SensorStreamHandler : EventChannel.StreamHandler {
  private var eventSink: EventChannel.EventSink? = null
  private var handler: Handler? = null
  private var runnable: Runnable? = null

  override fun onListen(arguments: Any?, events: EventChannel.EventSink?) {
    eventSink = events
    startSensorUpdates()
  }

  override fun onCancel(arguments: Any?) {
    stopSensorUpdates()
    eventSink = null
  }

  private fun startSensorUpdates() {
    handler = Handler(Looper.getMainLooper())
    runnable = object : Runnable {
      override fun run() {
        eventSink?.success(mapOf(
          "x" to 1.0,
          "y" to 2.0,
          "z" to 3.0,
          "timestamp" to System.currentTimeMillis()
        ))
        handler?.postDelayed(this, 100)
      }
    }
    handler?.post(runnable!!)
  }

  private fun stopSensorUpdates() {
    runnable?.let { handler?.removeCallbacks(it) }
  }
}
```

## 3. Federated Plugin Architecture

```
my_plugin/                          # App-facing package
├── lib/my_plugin.dart
├── pubspec.yaml
│   dependencies:
│     my_plugin_platform_interface: ^1.0.0
│     my_plugin_android: ^1.0.0     # Endorsed
│     my_plugin_ios: ^1.0.0         # Endorsed
│     my_plugin_web: ^1.0.0         # Endorsed

my_plugin_platform_interface/       # Platform interface
├── lib/
│   ├── my_plugin_platform_interface.dart
│   └── method_channel_my_plugin.dart

my_plugin_android/                  # Android implementation
├── android/
│   └── src/main/kotlin/.../MyPluginAndroid.kt
├── lib/my_plugin_android.dart
├── pubspec.yaml
│   flutter:
│     plugin:
│       implements: my_plugin
│       platforms:
│         android:
│           dartPluginClass: MyPluginAndroid

my_plugin_ios/                      # iOS implementation
├── ios/Classes/MyPluginIos.swift
├── lib/my_plugin_ios.dart

my_plugin_web/                      # Web implementation
├── lib/my_plugin_web.dart
```

### Platform Interface

```dart
// my_plugin_platform_interface/lib/my_plugin_platform_interface.dart
import 'package:plugin_platform_interface/plugin_platform_interface.dart';
import 'method_channel_my_plugin.dart';

abstract class MyPluginPlatform extends PlatformInterface {
  MyPluginPlatform() : super(token: _token);
  static final Object _token = Object();

  static MyPluginPlatform _instance = MethodChannelMyPlugin();
  static MyPluginPlatform get instance => _instance;
  static set instance(MyPluginPlatform instance) {
    PlatformInterface.verifyToken(instance, _token);
    _instance = instance;
  }

  Future<String?> getPlatformVersion() {
    throw UnimplementedError('getPlatformVersion() not implemented.');
  }
}
```

## 4. Error Handling

```dart
// Custom exceptions
class PluginException implements Exception {
  final String message;
  final String? code;
  final dynamic details;

  PluginException(this.message, {this.code, this.details});

  @override
  String toString() => 'PluginException: $message (code: $code)';
}

// Handle platform errors
Future<T> _invokeMethod<T>(String method, [dynamic arguments]) async {
  try {
    return await _channel.invokeMethod<T>(method, arguments) as T;
  } on PlatformException catch (e) {
    switch (e.code) {
      case 'PERMISSION_DENIED':
        throw PluginException('Permission denied', code: e.code);
      case 'NOT_AVAILABLE':
        throw PluginException('Feature not available', code: e.code);
      default:
        throw PluginException(e.message ?? 'Unknown error', code: e.code);
    }
  }
}
```

## 5. Publishing to pub.dev

```yaml
# pubspec.yaml
name: my_plugin
description: A Flutter plugin for...
version: 1.0.0
homepage: https://github.com/user/my_plugin
repository: https://github.com/user/my_plugin
issue_tracker: https://github.com/user/my_plugin/issues

environment:
  sdk: ">=3.0.0 <4.0.0"
  flutter: ">=3.3.0"

flutter:
  plugin:
    platforms:
      android:
        package: com.example.my_plugin
        pluginClass: MyPlugin
      ios:
        pluginClass: MyPlugin
```

```bash
# Validate before publishing
flutter pub publish --dry-run

# Publish
flutter pub publish

# Check pub.dev score factors:
# - README.md completeness
# - CHANGELOG.md presence
# - Example app
# - API documentation
# - Platform support
# - Test coverage
```

## Troubleshooting Guide

**Issue: MissingPluginException**
```
1. Hot restart (not hot reload) the app
2. Verify plugin is in pubspec.yaml dependencies
3. Run flutter clean && flutter pub get
4. Check plugin class registration
5. Verify channel name matches exactly
```

**Issue: iOS plugin not found**
```
1. cd ios && pod install
2. Check Podfile includes plugin
3. Verify Swift version compatibility
4. Check plugin registered in AppDelegate
```

**Issue: Android build fails**
```
1. Check minSdkVersion compatibility
2. Verify Kotlin version in build.gradle
3. Check for ProGuard rules if needed
4. Sync Gradle files
```

**Issue: EventChannel not receiving events**
```
1. Verify stream handler is registered
2. Check eventSink is not null
3. Ensure onListen returns nil (success)
4. Verify events are being sent to sink
5. Check stream subscription is active
```

## Plugin Quality Checklist

```
[ ] Clear README with installation & usage
[ ] CHANGELOG.md with version history
[ ] Working example app
[ ] Comprehensive dartdoc comments
[ ] Unit tests for Dart code
[ ] Integration tests for platform code
[ ] Error handling for all edge cases
[ ] Null safety
[ ] Platform support documented
[ ] Minimum SDK versions specified
```

---

**Build production-quality Flutter plugins for native integration.**
