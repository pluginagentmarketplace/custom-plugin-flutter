---
name: custom-plugin-flutter-skill-ui
description: 1700+ lines of Flutter UI mastery - widgets, layouts, Material Design, animations, responsive design with production-ready code examples and enterprise patterns.
---

# custom-plugin-flutter: UI Development Skill

## Quick Start - Production UI Pattern

```dart
class ResponsiveProductScreen extends ConsumerWidget {
  const ResponsiveProductScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isMobile = MediaQuery.of(context).size.width < 600;
    final productState = ref.watch(productProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Products'),
        elevation: 0,
      ),
      body: productState.when(
        loading: () => const LoadingWidget(),
        data: (products) => isMobile
            ? _MobileProductList(products: products)
            : _DesktopProductGrid(products: products),
        error: (error, st) => ErrorWidget(error: error.toString()),
      ),
    );
  }
}

class _MobileProductList extends StatelessWidget {
  final List<Product> products;
  const _MobileProductList({required this.products});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: products.length,
      itemBuilder: (context, index) => ProductCard(product: products[index]),
    );
  }
}

class _DesktopProductGrid extends StatelessWidget {
  final List<Product> products;
  const _DesktopProductGrid({required this.products});

  @override
  Widget build(BuildContext context) {
    return GridView.builder(
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 3,
        childAspectRatio: 0.8,
      ),
      itemCount: products.length,
      itemBuilder: (context, index) => ProductCard(product: products[index]),
    );
  }
}
```

## 1. Widget System Mastery

### Understanding the Widget Tree

**Stateless Widgets** - Pure, immutable widgets:
```dart
class PureWidget extends StatelessWidget {
  final String title;
  const PureWidget({required this.title});

  @override
  Widget build(BuildContext context) => Text(title);
}
```

**Stateful Widgets** - Managing internal state:
```dart
class CounterWidget extends StatefulWidget {
  const CounterWidget({Key? key}) : super(key: key);

  @override
  State<CounterWidget> createState() => _CounterWidgetState();
}

class _CounterWidgetState extends State<CounterWidget> {
  int _count = 0;

  void _increment() {
    setState(() => _count++);
  }

  @override
  void initState() {
    super.initState();
    // Initialize resources
  }

  @override
  void dispose() {
    // Clean up resources
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Count: $_count'),
        ElevatedButton(
          onPressed: _increment,
          child: const Text('Increment'),
        ),
      ],
    );
  }
}
```

**Const Constructors** - Preventing unnecessary rebuilds:
```dart
// ✅ Good - Const constructor
const SizedBox(height: 16, child: Text('Hello'))

// ❌ Bad - Non-const, rebuilds every time
SizedBox(height: 16, child: Text('Hello'))

// ✅ Make all widgets const when possible
class MyWidget extends StatelessWidget {
  const MyWidget({Key? key}) : super(key: key);
  
  @override
  Widget build(BuildContext context) => const Placeholder();
}
```

**Inherited Widgets** - Efficient state propagation:
```dart
class ThemeProvider extends InheritedWidget {
  final ThemeData theme;

  const ThemeProvider({
    required this.theme,
    required super.child,
    super.key,
  });

  static ThemeProvider of(BuildContext context) {
    final result = context.dependOnInheritedWidgetOfExactType<ThemeProvider>();
    assert(result != null, 'No ThemeProvider found in context');
    return result!;
  }

  @override
  bool updateShouldNotify(ThemeProvider oldWidget) => theme != oldWidget.theme;
}

// Usage
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ThemeProvider(
      theme: ThemeData.light(),
      child: MaterialApp(home: MyScreen()),
    );
  }
}

class MyScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final theme = ThemeProvider.of(context).theme;
    return Scaffold(
      backgroundColor: theme.scaffoldBackgroundColor,
    );
  }
}
```

## 2. Constraint-Based Layout System

### Understanding Constraints

**Basic Constraint Flow**:
```dart
// Parent imposes constraints on children
// Child sizes itself based on constraints
// Parent positions child based on alignment

Center(  // Imposes tight constraint
  child: Container(
    width: 200,
    height: 100,
    color: Colors.blue,
  ),
)
```

**Layout Widgets**:
```dart
// Row - horizontal layout
Row(
  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
  crossAxisAlignment: CrossAxisAlignment.center,
  children: [
    Text('Left'),
    Text('Middle'),
    Text('Right'),
  ],
)

// Column - vertical layout
Column(
  mainAxisSize: MainAxisSize.max,
  children: [
    Container(height: 100, color: Colors.red),
    Container(height: 100, color: Colors.blue),
    Container(height: 100, color: Colors.green),
  ],
)

// Flex - flexible layout
Flex(
  direction: Axis.horizontal,
  children: [
    Flexible(flex: 2, child: Container(color: Colors.red)),
    Flexible(flex: 1, child: Container(color: Colors.blue)),
  ],
)
```

**Advanced Layouts**:
```dart
// GridView - grid layout
GridView.builder(
  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
    crossAxisCount: 3,
    crossAxisSpacing: 8,
    mainAxisSpacing: 8,
  ),
  itemCount: 12,
  itemBuilder: (context, index) => Container(
    color: Colors.blue[100 * ((index % 9) + 1)],
  ),
)

// Stack - overlaying widgets
Stack(
  alignment: Alignment.bottomRight,
  children: [
    Image.asset('background.png'),
    Positioned(
      right: 16,
      bottom: 16,
      child: FloatingActionButton(onPressed: () {}),
    ),
  ],
)

// CustomMultiChildLayout - manual layout
CustomMultiChildLayout(
  delegate: MyLayoutDelegate(),
  children: [
    LayoutId(id: 'title', child: Text('Title')),
    LayoutId(id: 'body', child: Text('Body')),
  ],
)
```

## 3. Material Design 3 Implementation

### Theme Configuration

```dart
class AppTheme {
  static ThemeData lightTheme = ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.blue,
      brightness: Brightness.light,
    ),
    typography: Typography.material2021(
      platform: defaultTargetPlatform,
    ),
    appBarTheme: AppBarTheme(
      elevation: 0,
      backgroundColor: Colors.transparent,
    ),
    cardTheme: CardTheme(
      elevation: 2,
      margin: EdgeInsets.all(16),
    ),
  );

  static ThemeData darkTheme = ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.blue,
      brightness: Brightness.dark,
    ),
  );
}

// Usage
MaterialApp(
  theme: AppTheme.lightTheme,
  darkTheme: AppTheme.darkTheme,
  themeMode: ThemeMode.system,
)
```

### Material Components

```dart
// Modern AppBar
AppBar(
  title: Text('Title'),
  elevation: 0,
  backgroundColor: Theme.of(context).colorScheme.surface,
  foregroundColor: Theme.of(context).colorScheme.onSurface,
)

// Enhanced Button
ElevatedButton.icon(
  onPressed: () {},
  icon: Icon(Icons.send),
  label: Text('Send'),
  style: ElevatedButton.styleFrom(
    padding: EdgeInsets.symmetric(horizontal: 24, vertical: 12),
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
  ),
)

// Material TextField
TextField(
  decoration: InputDecoration(
    labelText: 'Enter name',
    hintText: 'John Doe',
    prefixIcon: Icon(Icons.person),
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(8),
    ),
    filled: true,
    fillColor: Colors.grey[100],
  ),
)

// Material Form
Form(
  key: _formKey,
  child: Column(
    children: [
      TextFormField(
        validator: (value) {
          if (value?.isEmpty ?? true) return 'Required';
          return null;
        },
      ),
      ElevatedButton(
        onPressed: () {
          if (_formKey.currentState!.validate()) {
            // Submit form
          }
        },
        child: Text('Submit'),
      ),
    ],
  ),
)
```

## 4. Animation Framework

### AnimationController Pattern

```dart
class AnimatedCounterWidget extends StatefulWidget {
  const AnimatedCounterWidget();

  @override
  State<AnimatedCounterWidget> createState() => _AnimatedCounterWidgetState();
}

class _AnimatedCounterWidgetState extends State<AnimatedCounterWidget>
    with TickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;
  int _count = 0;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Duration(milliseconds: 300),
      vsync: this,
    );
    _animation = Tween<double>(begin: 1, end: 0.8).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );
  }

  void _increment() {
    setState(() => _count++);
    _controller.forward().then((_) => _controller.reverse());
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ScaleTransition(
      scale: _animation,
      child: GestureDetector(
        onTap: _increment,
        child: Container(
          width: 100,
          height: 100,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: Colors.blue,
          ),
          child: Center(
            child: Text(
              '$_count',
              style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                    color: Colors.white,
                  ),
            ),
          ),
        ),
      ),
    );
  }
}
```

### Implicit Animations

```dart
// AnimatedContainer - animate properties smoothly
class AnimatedBoxWidget extends StatefulWidget {
  @override
  State<AnimatedBoxWidget> createState() => _AnimatedBoxWidgetState();
}

class _AnimatedBoxWidgetState extends State<AnimatedBoxWidget> {
  bool _expanded = false;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: GestureDetector(
        onTap: () => setState(() => _expanded = !_expanded),
        child: AnimatedContainer(
          duration: Duration(milliseconds: 500),
          width: _expanded ? 300 : 100,
          height: _expanded ? 300 : 100,
          decoration: BoxDecoration(
            color: _expanded ? Colors.blue : Colors.red,
            borderRadius: BorderRadius.circular(_expanded ? 16 : 8),
          ),
          child: Center(
            child: AnimatedOpacity(
              opacity: _expanded ? 1 : 0,
              duration: Duration(milliseconds: 500),
              child: Text('Expanded'),
            ),
          ),
        ),
      ),
    );
  }
}
```

## 5. Responsive Design Pattern

```dart
class ResponsiveWidget extends StatelessWidget {
  final Widget Function(BuildContext) mobileBuilder;
  final Widget Function(BuildContext) tabletBuilder;
  final Widget Function(BuildContext) desktopBuilder;

  const ResponsiveWidget({
    required this.mobileBuilder,
    required this.tabletBuilder,
    required this.desktopBuilder,
  });

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;

    if (width < 600) {
      return mobileBuilder(context);
    } else if (width < 1200) {
      return tabletBuilder(context);
    } else {
      return desktopBuilder(context);
    }
  }
}

// Usage
ResponsiveWidget(
  mobileBuilder: (context) => MobileLayout(),
  tabletBuilder: (context) => TabletLayout(),
  desktopBuilder: (context) => DesktopLayout(),
)
```

## 6. Accessibility Best Practices

```dart
class AccessibleWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Semantics(
      button: true,
      label: 'Submit form',
      enabled: true,
      onTap: () {},
      child: Container(
        constraints: BoxConstraints(minHeight: 48, minWidth: 48),
        decoration: BoxDecoration(
          color: Colors.blue,
          borderRadius: BorderRadius.circular(8),
        ),
        child: Center(
          child: Text(
            'Submit',
            style: TextStyle(fontSize: 16), // Respect system font scaling
          ),
        ),
      ),
    );
  }
}
```

## 7. Performance Optimization Tips

- ✅ Use `const` constructors everywhere possible
- ✅ Extract widgets to separate classes to limit rebuilds
- ✅ Use `RepaintBoundary` for expensive rendering
- ✅ Use `ListView.builder` instead of `ListView`
- ✅ Cache images with `CachedNetworkImage`
- ✅ Profile with DevTools regularly
- ✅ Use `LayoutBuilder` for responsive design
- ✅ Prefer `SingleChildScrollView` over custom scrolling

## 8. Custom Widget Template

```dart
class CustomButton extends StatelessWidget {
  final VoidCallback onPressed;
  final String label;
  final ButtonSize size;

  const CustomButton({
    required this.onPressed,
    required this.label,
    this.size = ButtonSize.medium,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      child: InkWell(
        onTap: onPressed,
        child: Container(
          padding: _paddingForSize(size),
          decoration: BoxDecoration(
            color: Theme.of(context).primaryColor,
            borderRadius: BorderRadius.circular(8),
          ),
          child: Text(
            label,
            style: Theme.of(context).textTheme.labelLarge,
          ),
        ),
      ),
    );
  }

  EdgeInsets _paddingForSize(ButtonSize size) {
    switch (size) {
      case ButtonSize.small:
        return EdgeInsets.symmetric(horizontal: 12, vertical: 8);
      case ButtonSize.medium:
        return EdgeInsets.symmetric(horizontal: 16, vertical: 12);
      case ButtonSize.large:
        return EdgeInsets.symmetric(horizontal: 24, vertical: 16);
    }
  }
}

enum ButtonSize { small, medium, large }
```

---

**Master Flutter UI development with this comprehensive skill reference.**
