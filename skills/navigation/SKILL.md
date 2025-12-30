---
name: navigation
description: Flutter navigation with Navigator 2.0 and routing packages
sasmp_version: "2.0.0"
eqhm_version: "1.1.0"
bonded_agent: 01-flutter-ui-development
bond_type: PRIMARY_BOND
---

# Flutter Navigation Skill

## Overview
Implement navigation in Flutter apps using Navigator 1.0, 2.0, and popular routing packages like GoRouter. Master deep linking, nested navigation, and web URL handling.

## Topics Covered

### Navigator 1.0
- Push and pop navigation
- Named routes
- Route arguments
- Modal routes
- Navigation observers

### Navigator 2.0
- Router and RouteInformationParser
- RouterDelegate
- Declarative navigation
- Deep linking
- Browser history

### GoRouter
- Route configuration
- Path parameters
- Query parameters
- Redirect logic
- ShellRoute for nested navigation

### Advanced Navigation
- Bottom navigation with state
- Drawer navigation
- Tab navigation
- Nested navigators
- Route guards

### Platform Integration
- Deep links setup
- Universal links (iOS)
- App links (Android)
- Web URL handling

## Core Patterns

### 🔷 GoRouter Setup (Recommended)

```dart
// lib/router/app_router.dart
import 'package:go_router/go_router.dart';

final appRouter = GoRouter(
  initialLocation: '/',
  debugLogDiagnostics: true,
  redirect: (context, state) {
    final isLoggedIn = authService.isLoggedIn;
    final isLoggingIn = state.matchedLocation == '/login';

    if (!isLoggedIn && !isLoggingIn) return '/login';
    if (isLoggedIn && isLoggingIn) return '/';
    return null;
  },
  routes: [
    GoRoute(
      path: '/',
      name: 'home',
      builder: (context, state) => const HomePage(),
      routes: [
        GoRoute(
          path: 'product/:id',
          name: 'product',
          builder: (context, state) {
            final productId = state.pathParameters['id']!;
            return ProductPage(productId: productId);
          },
        ),
        GoRoute(
          path: 'search',
          name: 'search',
          builder: (context, state) {
            final query = state.uri.queryParameters['q'] ?? '';
            return SearchPage(query: query);
          },
        ),
      ],
    ),
    GoRoute(
      path: '/login',
      name: 'login',
      builder: (context, state) => const LoginPage(),
    ),
  ],
  errorBuilder: (context, state) => ErrorPage(error: state.error),
);

// Usage in MaterialApp
MaterialApp.router(
  routerConfig: appRouter,
  title: 'My App',
)
```

### 🔶 ShellRoute for Nested Navigation

```dart
// Bottom navigation with persistent shell
final appRouter = GoRouter(
  initialLocation: '/home',
  routes: [
    ShellRoute(
      navigatorKey: _shellNavigatorKey,
      builder: (context, state, child) {
        return ScaffoldWithNavBar(child: child);
      },
      routes: [
        GoRoute(
          path: '/home',
          name: 'home',
          pageBuilder: (context, state) => const NoTransitionPage(
            child: HomePage(),
          ),
        ),
        GoRoute(
          path: '/explore',
          name: 'explore',
          pageBuilder: (context, state) => const NoTransitionPage(
            child: ExplorePage(),
          ),
        ),
        GoRoute(
          path: '/profile',
          name: 'profile',
          pageBuilder: (context, state) => const NoTransitionPage(
            child: ProfilePage(),
          ),
        ),
      ],
    ),
    // Routes outside the shell (full screen)
    GoRoute(
      path: '/settings',
      name: 'settings',
      builder: (context, state) => const SettingsPage(),
    ),
  ],
);

// ScaffoldWithNavBar widget
class ScaffoldWithNavBar extends StatelessWidget {
  final Widget child;
  const ScaffoldWithNavBar({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: child,
      bottomNavigationBar: NavigationBar(
        selectedIndex: _calculateSelectedIndex(context),
        onDestinationSelected: (index) => _onItemTapped(index, context),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.explore), label: 'Explore'),
          NavigationDestination(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }

  int _calculateSelectedIndex(BuildContext context) {
    final location = GoRouterState.of(context).matchedLocation;
    if (location.startsWith('/home')) return 0;
    if (location.startsWith('/explore')) return 1;
    if (location.startsWith('/profile')) return 2;
    return 0;
  }

  void _onItemTapped(int index, BuildContext context) {
    switch (index) {
      case 0:
        context.goNamed('home');
      case 1:
        context.goNamed('explore');
      case 2:
        context.goNamed('profile');
    }
  }
}
```

### 🟢 Route Guards and Redirect

```dart
// Authentication-aware routing
final appRouter = GoRouter(
  refreshListenable: authNotifier, // Refresh on auth changes
  redirect: (context, state) {
    final isLoggedIn = authNotifier.isLoggedIn;
    final isOnboarded = prefsService.isOnboarded;
    final location = state.matchedLocation;

    // Onboarding check
    if (!isOnboarded && location != '/onboarding') {
      return '/onboarding';
    }

    // Auth check
    final authRoutes = ['/login', '/register', '/forgot-password'];
    final isAuthRoute = authRoutes.contains(location);

    if (!isLoggedIn && !isAuthRoute) {
      return '/login?redirect=${Uri.encodeComponent(location)}';
    }

    if (isLoggedIn && isAuthRoute) {
      final redirect = state.uri.queryParameters['redirect'];
      return redirect != null ? Uri.decodeComponent(redirect) : '/';
    }

    return null;
  },
  routes: [...],
);

// Auth notifier for refresh
class AuthNotifier extends ChangeNotifier {
  bool _isLoggedIn = false;
  bool get isLoggedIn => _isLoggedIn;

  void login() {
    _isLoggedIn = true;
    notifyListeners();
  }

  void logout() {
    _isLoggedIn = false;
    notifyListeners();
  }
}
```

### 🟣 Custom Page Transitions

```dart
GoRoute(
  path: '/details/:id',
  name: 'details',
  pageBuilder: (context, state) {
    return CustomTransitionPage(
      key: state.pageKey,
      child: DetailsPage(id: state.pathParameters['id']!),
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        return SlideTransition(
          position: Tween<Offset>(
            begin: const Offset(1, 0),
            end: Offset.zero,
          ).animate(CurvedAnimation(
            parent: animation,
            curve: Curves.easeInOutCubic,
          )),
          child: child,
        );
      },
      transitionDuration: const Duration(milliseconds: 300),
    );
  },
)

// Fade transition helper
class FadeTransitionPage extends CustomTransitionPage {
  FadeTransitionPage({
    required super.child,
    super.key,
  }) : super(
          transitionsBuilder: (context, animation, secondaryAnimation, child) {
            return FadeTransition(opacity: animation, child: child);
          },
        );
}
```

### 🔴 Deep Links Configuration

```dart
// android/app/src/main/AndroidManifest.xml
/*
<intent-filter android:autoVerify="true">
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />
  <data
    android:scheme="https"
    android:host="example.com"
    android:pathPrefix="/app" />
</intent-filter>
*/

// ios/Runner/Info.plist
/*
<key>FlutterDeepLinkingEnabled</key>
<true/>
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>myapp</string>
    </array>
  </dict>
</array>
*/

// Handle deep links in GoRouter
final appRouter = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/product/:id',
      builder: (context, state) {
        // Handles: myapp://product/123
        // Handles: https://example.com/app/product/123
        return ProductPage(productId: state.pathParameters['id']!);
      },
    ),
  ],
);
```

### 🟠 Navigator 1.0 Patterns (Legacy)

```dart
// Named routes setup
MaterialApp(
  initialRoute: '/',
  onGenerateRoute: (settings) {
    switch (settings.name) {
      case '/':
        return MaterialPageRoute(builder: (_) => const HomePage());
      case '/product':
        final args = settings.arguments as ProductArgs;
        return MaterialPageRoute(
          builder: (_) => ProductPage(product: args.product),
        );
      default:
        return MaterialPageRoute(builder: (_) => const NotFoundPage());
    }
  },
)

// Navigation with arguments
Navigator.pushNamed(
  context,
  '/product',
  arguments: ProductArgs(product: product),
);

// Return value from route
final result = await Navigator.push<bool>(
  context,
  MaterialPageRoute(builder: (_) => const ConfirmPage()),
);
if (result == true) {
  // User confirmed
}

// Pop until specific route
Navigator.popUntil(context, ModalRoute.withName('/'));

// Replace current route
Navigator.pushReplacementNamed(context, '/home');
```

### 🔵 Modal Routes

```dart
// Bottom sheet navigation
void showProductOptions(BuildContext context, Product product) {
  showModalBottomSheet(
    context: context,
    isScrollControlled: true,
    backgroundColor: Colors.transparent,
    builder: (context) => DraggableScrollableSheet(
      initialChildSize: 0.5,
      minChildSize: 0.3,
      maxChildSize: 0.9,
      builder: (context, scrollController) => Container(
        decoration: const BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
        ),
        child: ProductOptionsSheet(
          product: product,
          scrollController: scrollController,
        ),
      ),
    ),
  );
}

// Dialog navigation
Future<bool?> showConfirmDialog(BuildContext context, String message) {
  return showDialog<bool>(
    context: context,
    barrierDismissible: false,
    builder: (context) => AlertDialog(
      title: const Text('Confirm'),
      content: Text(message),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context, false),
          child: const Text('Cancel'),
        ),
        FilledButton(
          onPressed: () => Navigator.pop(context, true),
          child: const Text('Confirm'),
        ),
      ],
    ),
  );
}

// Full-screen modal
Navigator.of(context).push(
  MaterialPageRoute(
    fullscreenDialog: true,
    builder: (context) => const CreatePostPage(),
  ),
);
```

## Type-Safe Navigation Extension

```dart
// lib/router/routes.dart
extension AppRouterExtension on BuildContext {
  void goToHome() => goNamed('home');

  void goToProduct(String productId) => goNamed(
        'product',
        pathParameters: {'id': productId},
      );

  void goToSearch({String? query}) => goNamed(
        'search',
        queryParameters: query != null ? {'q': query} : {},
      );

  void goToLogin({String? redirect}) => goNamed(
        'login',
        queryParameters: redirect != null ? {'redirect': redirect} : {},
      );
}

// Usage
context.goToProduct('abc123');
context.goToSearch(query: 'flutter');
```

## Troubleshooting Guide

### Common Issues

#### 1. Deep Link Not Working
```
❌ Symptom: App doesn't open from deep link

✅ Debug Checklist:
□ Verify AndroidManifest.xml intent-filter
□ Check Info.plist URL schemes
□ Test with: adb shell am start -a android.intent.action.VIEW -d "myapp://path"
□ For iOS: xcrun simctl openurl booted "myapp://path"
□ Ensure FlutterDeepLinkingEnabled is true
```

#### 2. GoRouter Redirect Loop
```
❌ Error: Maximum redirects exceeded

✅ Solutions:
1. Check redirect logic for circular conditions
2. Ensure auth routes are excluded from auth check
3. Add null return for allowed routes
4. Debug with debugLogDiagnostics: true
```

#### 3. Bottom Nav State Lost
```
❌ Symptom: Tab state resets on navigation

✅ Solutions:
1. Use ShellRoute with separate navigators
2. Use AutomaticKeepAliveClientMixin in tab pages
3. Store scroll positions in provider/bloc
4. Use IndexedStack to preserve tab state
```

#### 4. Browser Back Button Issues
```
❌ Symptom: Back button doesn't work on web

✅ Solutions:
1. Ensure GoRouter is correctly configured
2. Use context.go() for replacing, context.push() for adding
3. Check that routes have unique paths
4. Test browser history with DevTools
```

## Debug Commands

```bash
# Test deep links on Android
adb shell am start -a android.intent.action.VIEW \
  -d "https://example.com/product/123" \
  com.example.app

# Test deep links on iOS
xcrun simctl openurl booted "myapp://product/123"

# Verify Android App Links
adb shell pm get-app-links com.example.app

# Debug GoRouter (add to router config)
# debugLogDiagnostics: true
```

## Integration Points

| Agent | Integration |
|-------|-------------|
| 01-UI-Development | Navigation in UI flows |
| 02-State-Management | Auth state for routing |
| 06-Testing-QA | Navigation testing |
| 07-DevOps | Deep link configuration |

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Deep Link Success | 100% | Analytics |
| Navigation Speed | <100ms | DevTools |
| Back Stack Integrity | 100% | Manual test |
| Web URL Sync | 100% | Browser test |

## Prerequisites
- Flutter widget basics
- State management
- BuildContext understanding

## Learning Outcomes
- Implement declarative routing
- Handle deep links
- Build nested navigation
- Configure web navigation

## EQHM Compliance

- ✅ **Ethical**: Predictable navigation behavior
- ✅ **Quality**: Type-safe route parameters
- ✅ **Honest**: Clear route structure
- ✅ **Maintainable**: Centralized routing config

---

*This skill enables robust, scalable navigation in Flutter apps.*
