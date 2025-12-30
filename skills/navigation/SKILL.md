---
name: custom-plugin-flutter-skill-navigation
description: Production-grade Flutter navigation mastery - Navigator 2.0, GoRouter, deep linking, nested navigation, route guards, web URL handling with comprehensive code examples
sasmp_version: "1.3.0"
bonded_agent: 01-flutter-ui-development
bond_type: PRIMARY_BOND
---

# custom-plugin-flutter: Navigation Skill

## Quick Start - GoRouter Production Setup

```dart
// router.dart
final router = GoRouter(
  initialLocation: '/',
  debugLogDiagnostics: true,
  refreshListenable: authNotifier,
  redirect: (context, state) {
    final isLoggedIn = authNotifier.isLoggedIn;
    final isLoggingIn = state.matchedLocation == '/login';

    if (!isLoggedIn && !isLoggingIn) return '/login';
    if (isLoggedIn && isLoggingIn) return '/';
    return null;
  },
  errorBuilder: (context, state) => ErrorPage(error: state.error),
  routes: [
    GoRoute(
      path: '/',
      name: 'home',
      builder: (context, state) => const HomePage(),
    ),
    GoRoute(
      path: '/login',
      name: 'login',
      builder: (context, state) => const LoginPage(),
    ),
    GoRoute(
      path: '/products/:id',
      name: 'product',
      builder: (context, state) {
        final id = state.pathParameters['id']!;
        return ProductPage(productId: id);
      },
    ),
    ShellRoute(
      builder: (context, state, child) => MainShell(child: child),
      routes: [
        GoRoute(path: '/dashboard', builder: (_, __) => DashboardPage()),
        GoRoute(path: '/settings', builder: (_, __) => SettingsPage()),
      ],
    ),
  ],
);

// main.dart
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: router,
    );
  }
}

// Navigation usage
context.go('/products/123');                    // Replace
context.push('/products/123');                  // Push
context.goNamed('product', pathParameters: {'id': '123'});
context.pop();                                  // Go back
```

## 1. Navigator 1.0 (Imperative)

### Basic Navigation

```dart
// Push new route
Navigator.push(
  context,
  MaterialPageRoute(builder: (context) => DetailPage()),
);

// Pop current route
Navigator.pop(context);

// Pop with result
Navigator.pop(context, 'result_data');

// Push and remove until
Navigator.pushAndRemoveUntil(
  context,
  MaterialPageRoute(builder: (_) => HomePage()),
  (route) => false,  // Remove all
);

// Push replacement
Navigator.pushReplacement(
  context,
  MaterialPageRoute(builder: (_) => NewPage()),
);
```

### Named Routes

```dart
// Define routes
MaterialApp(
  initialRoute: '/',
  routes: {
    '/': (context) => HomePage(),
    '/detail': (context) => DetailPage(),
    '/settings': (context) => SettingsPage(),
  },
  onGenerateRoute: (settings) {
    if (settings.name?.startsWith('/product/') ?? false) {
      final id = settings.name!.split('/').last;
      return MaterialPageRoute(
        builder: (_) => ProductPage(id: id),
      );
    }
    return null;
  },
  onUnknownRoute: (settings) {
    return MaterialPageRoute(builder: (_) => NotFoundPage());
  },
);

// Navigate with arguments
Navigator.pushNamed(
  context,
  '/detail',
  arguments: {'id': 123, 'title': 'Product'},
);

// Retrieve arguments
final args = ModalRoute.of(context)?.settings.arguments as Map?;
```

## 2. Navigator 2.0 (Declarative)

### Router Configuration

```dart
class AppRouterDelegate extends RouterDelegate<AppRoutePath>
    with ChangeNotifier, PopNavigatorRouterDelegateMixin<AppRoutePath> {
  @override
  final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();

  AppRoutePath _currentPath = AppRoutePath.home();

  @override
  AppRoutePath get currentConfiguration => _currentPath;

  @override
  Widget build(BuildContext context) {
    return Navigator(
      key: navigatorKey,
      pages: [
        MaterialPage(
          key: ValueKey('home'),
          child: HomePage(),
        ),
        if (_currentPath.isProductPage)
          MaterialPage(
            key: ValueKey('product-${_currentPath.productId}'),
            child: ProductPage(id: _currentPath.productId!),
          ),
      ],
      onPopPage: (route, result) {
        if (!route.didPop(result)) return false;
        _currentPath = AppRoutePath.home();
        notifyListeners();
        return true;
      },
    );
  }

  @override
  Future<void> setNewRoutePath(AppRoutePath path) async {
    _currentPath = path;
    notifyListeners();
  }

  void goToProduct(String id) {
    _currentPath = AppRoutePath.product(id);
    notifyListeners();
  }
}

class AppRouteInformationParser extends RouteInformationParser<AppRoutePath> {
  @override
  Future<AppRoutePath> parseRouteInformation(
    RouteInformation routeInformation,
  ) async {
    final uri = routeInformation.uri;

    if (uri.pathSegments.isEmpty) {
      return AppRoutePath.home();
    }

    if (uri.pathSegments.length == 2 && uri.pathSegments[0] == 'product') {
      return AppRoutePath.product(uri.pathSegments[1]);
    }

    return AppRoutePath.home();
  }

  @override
  RouteInformation restoreRouteInformation(AppRoutePath path) {
    if (path.isHomePage) {
      return RouteInformation(uri: Uri.parse('/'));
    }
    if (path.isProductPage) {
      return RouteInformation(uri: Uri.parse('/product/${path.productId}'));
    }
    return RouteInformation(uri: Uri.parse('/'));
  }
}
```

## 3. GoRouter Advanced Patterns

### Nested Navigation with ShellRoute

```dart
final router = GoRouter(
  routes: [
    ShellRoute(
      navigatorKey: _shellNavigatorKey,
      builder: (context, state, child) {
        return ScaffoldWithNavBar(child: child);
      },
      routes: [
        GoRoute(
          path: '/home',
          pageBuilder: (context, state) => NoTransitionPage(
            child: HomePage(),
          ),
        ),
        GoRoute(
          path: '/search',
          pageBuilder: (context, state) => NoTransitionPage(
            child: SearchPage(),
          ),
        ),
        GoRoute(
          path: '/profile',
          pageBuilder: (context, state) => NoTransitionPage(
            child: ProfilePage(),
          ),
        ),
      ],
    ),
    // Routes outside shell (full screen)
    GoRoute(
      path: '/product/:id',
      parentNavigatorKey: _rootNavigatorKey,
      builder: (context, state) => ProductPage(
        id: state.pathParameters['id']!,
      ),
    ),
  ],
);

class ScaffoldWithNavBar extends StatelessWidget {
  final Widget child;
  const ScaffoldWithNavBar({required this.child});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: child,
      bottomNavigationBar: NavigationBar(
        selectedIndex: _calculateSelectedIndex(context),
        onDestinationSelected: (index) => _onItemTapped(index, context),
        destinations: [
          NavigationDestination(icon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.search), label: 'Search'),
          NavigationDestination(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }

  int _calculateSelectedIndex(BuildContext context) {
    final location = GoRouterState.of(context).matchedLocation;
    if (location.startsWith('/home')) return 0;
    if (location.startsWith('/search')) return 1;
    if (location.startsWith('/profile')) return 2;
    return 0;
  }

  void _onItemTapped(int index, BuildContext context) {
    switch (index) {
      case 0: context.go('/home');
      case 1: context.go('/search');
      case 2: context.go('/profile');
    }
  }
}
```

### Route Guards & Redirects

```dart
GoRouter(
  redirect: (context, state) {
    final isLoggedIn = ref.read(authProvider).isLoggedIn;
    final isOnboarded = ref.read(onboardingProvider).completed;
    final location = state.matchedLocation;

    // Onboarding flow
    if (!isOnboarded && !location.startsWith('/onboarding')) {
      return '/onboarding';
    }

    // Auth flow
    if (!isLoggedIn) {
      final publicRoutes = ['/login', '/register', '/forgot-password'];
      if (!publicRoutes.contains(location)) {
        return '/login?redirect=${Uri.encodeComponent(location)}';
      }
    }

    // Already logged in, redirect away from auth pages
    if (isLoggedIn && location == '/login') {
      final redirect = state.uri.queryParameters['redirect'];
      return redirect ?? '/';
    }

    return null; // No redirect
  },
)
```

## 4. Deep Linking

### iOS Universal Links

```xml
<!-- ios/Runner/Runner.entitlements -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN">
<plist version="1.0">
<dict>
  <key>com.apple.developer.associated-domains</key>
  <array>
    <string>applinks:example.com</string>
  </array>
</dict>
</plist>
```

### Android App Links

```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<intent-filter android:autoVerify="true">
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />
  <data
    android:scheme="https"
    android:host="example.com"
    android:pathPrefix="/product" />
</intent-filter>
```

### Handling Deep Links

```dart
// GoRouter handles automatically
GoRoute(
  path: '/product/:id',
  builder: (context, state) {
    final id = state.pathParameters['id']!;
    final source = state.uri.queryParameters['utm_source'];
    return ProductPage(id: id, source: source);
  },
)

// Manual handling
import 'package:app_links/app_links.dart';

final appLinks = AppLinks();

// Listen for links
appLinks.uriLinkStream.listen((uri) {
  router.go(uri.path + (uri.query.isNotEmpty ? '?${uri.query}' : ''));
});

// Get initial link
final initialUri = await appLinks.getInitialAppLink();
if (initialUri != null) {
  router.go(initialUri.path);
}
```

## 5. Query Parameters & Extras

```dart
// Query parameters
GoRoute(
  path: '/search',
  builder: (context, state) {
    final query = state.uri.queryParameters['q'] ?? '';
    final page = int.tryParse(state.uri.queryParameters['page'] ?? '1') ?? 1;
    return SearchPage(query: query, page: page);
  },
)

// Navigate with query params
context.go('/search?q=flutter&page=1');

// Type-safe extras
context.push('/product/123', extra: Product(id: '123', name: 'Widget'));

// Retrieve extras
GoRoute(
  path: '/product/:id',
  builder: (context, state) {
    final product = state.extra as Product?;
    final id = state.pathParameters['id']!;
    return ProductPage(product: product, id: id);
  },
)
```

## Troubleshooting Guide

**Issue: Deep link not working**
```
1. Verify Associated Domains (iOS) / App Links (Android)
2. Check aasa file at .well-known/apple-app-site-association
3. Check assetlinks.json at .well-known/assetlinks.json
4. Test: adb shell am start -a android.intent.action.VIEW -d "https://..."
5. Verify intent-filter in AndroidManifest.xml
```

**Issue: Route not found**
```
1. Check path matches exactly (case-sensitive)
2. Verify route is registered in GoRouter
3. Check for typos in pathParameters
4. Enable debugLogDiagnostics: true
```

**Issue: Back button doesn't work correctly**
```
1. Use context.push() instead of context.go()
2. Check ShellRoute configuration
3. Verify parentNavigatorKey assignments
4. Handle PopScope for custom back behavior
```

**Issue: State lost on navigation**
```
1. Use ShellRoute to preserve state
2. Store state in provider/bloc above Navigator
3. Use PageStorageKey for scroll position
4. Consider using AutomaticKeepAliveClientMixin
```

## Navigation Pattern Selection

| Scenario | Solution |
|----------|----------|
| Simple app | Navigator 1.0 |
| Web/Deep links | GoRouter |
| Complex flows | Navigator 2.0 |
| Tab navigation | ShellRoute |
| Auth guards | GoRouter redirect |
| Modal screens | showModalBottomSheet |

---

**Master Flutter navigation for seamless user experiences.**
