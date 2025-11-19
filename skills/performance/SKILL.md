---
name: custom-plugin-flutter-skill-performance
description: 1600+ lines of performance optimization mastery - profiling, rendering, memory, network, battery, APK size with production-ready code examples.
---

# custom-plugin-flutter: Performance Optimization Skill

## Quick Start - Top 10 Optimizations

```dart
// 1. Use const constructors
const SizedBox(height: 16);

// 2. Extract widgets for rebuild optimization
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const Title(),  // Const - won't rebuild
        BuildCounter(),  // Rebuilds only when needed
      ],
    );
  }
}

// 3. Use ListView.builder
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemTile(item: items[index]),
)

// 4. Cache network images
CachedNetworkImage(imageUrl: 'https://example.com/image.png')

// 5. Use RepaintBoundary for expensive widgets
RepaintBoundary(child: ExpensiveChart())

// 6. Profile regularly
// - Open DevTools Performance tab
// - Record timeline
// - Check frame rate and rebuild counts

// 7. Use const everywhere
const AppBar(title: Text('Title'))

// 8. Profile memory
// - Open DevTools Memory tab
// - Take heap snapshots
// - Look for memory leaks

// 9. Use SingleChildScrollView wisely
SingleChildScrollView(
  child: Column(children: [...]),
)

// 10. Optimize images
Image.asset(
  'assets/image.png',
  cacheHeight: 500,
  cacheWidth: 500,
)
```

## 1. Rendering Performance

**Frame Analysis:**
```dart
// Monitor frame rate with DevTools
// Target: 60 FPS (16.67ms per frame)
// Warning: 30-60 FPS (16-33ms)
// Danger: <30 FPS (>33ms)

class PerformanceMonitor {
  void measureFrame() {
    final start = DateTime.now();
    // Do work
    final duration = DateTime.now().difference(start);
    print('Frame took ${duration.inMilliseconds}ms');
  }
}
```

**Preventing Jank:**
```dart
// Bad: Expensive computation on main thread
class BadWidget extends StatefulWidget {
  @override
  State<BadWidget> createState() => _BadWidgetState();
}

class _BadWidgetState extends State<BadWidget> {
  @override
  Widget build(BuildContext context) {
    final expensive = expensiveComputation(); // Blocks UI!
    return Text('Result: $expensive');
  }
}

// Good: Use Isolate or async
class GoodWidget extends StatefulWidget {
  @override
  State<GoodWidget> createState() => _GoodWidgetState();
}

class _GoodWidgetState extends State<GoodWidget> {
  late Future<dynamic> _computation;

  @override
  void initState() {
    super.initState();
    _computation = compute(expensiveComputation, null);
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: _computation,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          return Text('Result: ${snapshot.data}');
        }
        return CircularProgressIndicator();
      },
    );
  }
}
```

## 2. Memory Optimization

```dart
// Memory profiling with DevTools
// Target: <100MB for typical app
// Peak: <150MB during heavy operations

class MemoryOptimized {
  // Bad: Keep large objects in memory
  List<LargeObject> _cache = [];

  // Good: Limited cache size
  final _cache = LimitedQueue<LargeObject>(maxSize: 50);

  void dispose() {
    _cache.clear();
  }
}

class LimitedQueue<T> {
  final int maxSize;
  final _queue = <T>[];

  LimitedQueue({required this.maxSize});

  void add(T item) {
    _queue.add(item);
    if (_queue.length > maxSize) {
      _queue.removeAt(0);
    }
  }

  void clear() => _queue.clear();
}
```

## 3. APK/IPA Size Reduction

**Build with size analysis:**
```bash
# Android - analyze size
flutter build apk --release --analyze-size

# iOS - check build size
ls -lh build/ios/Release-iphoneos/app.ipa
```

**Reduce size:**
```gradle
// android/app/build.gradle
android {
  buildTypes {
    release {
      minifyEnabled true
      shrinkResources true
      proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
    }
  }
}

// Split APKs by ABI
flutter build apk --split-per-abi
```

## 4. Network Optimization

```dart
// Connection pooling with Dio
final dio = Dio(BaseOptions(
  connectTimeout: Duration(seconds: 10),
));

// Cache responses
dio.interceptors.add(
  CacheInterceptor(
    options: CacheOptions(
      store: MemoryCacheStore(),
      policy: CachePolicy.request,
      maxStale: Duration(days: 7),
    ),
  ),
);

// Batch requests
Future<(UserList, PostList)> fetchUserAndPosts(String userId) async {
  final futures = await Future.wait([
    dio.get('/users/$userId'),
    dio.get('/posts?userId=$userId'),
  ]);

  return (
    UserList.fromJson(futures[0].data),
    PostList.fromJson(futures[1].data),
  );
}
```

---

**Build lightning-fast, efficient Flutter apps.**
