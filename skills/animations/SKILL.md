---
name: custom-plugin-flutter-skill-animations
description: Production-grade Flutter animations mastery - Implicit and explicit animations, AnimationController, Hero transitions, physics-based motion, Lottie/Rive integration, 60fps optimization with comprehensive code examples
sasmp_version: "1.3.0"
bonded_agent: 01-flutter-ui-development
bond_type: PRIMARY_BOND
---

# custom-plugin-flutter: Animations Skill

## Quick Start - Production Animation Pattern

```dart
class AnimatedProductCard extends StatefulWidget {
  final Product product;
  final bool isSelected;

  const AnimatedProductCard({
    required this.product,
    required this.isSelected,
  });

  @override
  State<AnimatedProductCard> createState() => _AnimatedProductCardState();
}

class _AnimatedProductCardState extends State<AnimatedProductCard>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final Animation<double> _scaleAnimation;
  late final Animation<double> _opacityAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 200),
      vsync: this,
    );

    _scaleAnimation = Tween<double>(begin: 1.0, end: 0.95).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );

    _opacityAnimation = Tween<double>(begin: 1.0, end: 0.8).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _onTapDown(TapDownDetails details) => _controller.forward();
  void _onTapUp(TapUpDetails details) => _controller.reverse();
  void _onTapCancel() => _controller.reverse();

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: _onTapDown,
      onTapUp: _onTapUp,
      onTapCancel: _onTapCancel,
      child: AnimatedBuilder(
        animation: _controller,
        builder: (context, child) {
          return Transform.scale(
            scale: _scaleAnimation.value,
            child: Opacity(
              opacity: _opacityAnimation.value,
              child: child,
            ),
          );
        },
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 300),
          decoration: BoxDecoration(
            border: Border.all(
              color: widget.isSelected ? Colors.blue : Colors.grey,
              width: widget.isSelected ? 2 : 1,
            ),
            borderRadius: BorderRadius.circular(12),
          ),
          child: ProductContent(product: widget.product),
        ),
      ),
    );
  }
}
```

## 1. Implicit Animations

### Built-in Animated Widgets

```dart
// AnimatedContainer - Animate multiple properties
AnimatedContainer(
  duration: Duration(milliseconds: 300),
  curve: Curves.easeInOut,
  width: isExpanded ? 300 : 100,
  height: isExpanded ? 200 : 100,
  decoration: BoxDecoration(
    color: isActive ? Colors.blue : Colors.grey,
    borderRadius: BorderRadius.circular(isExpanded ? 16 : 8),
    boxShadow: isActive ? [BoxShadow(blurRadius: 10)] : [],
  ),
  child: content,
)

// AnimatedOpacity
AnimatedOpacity(
  opacity: isVisible ? 1.0 : 0.0,
  duration: Duration(milliseconds: 200),
  child: content,
)

// AnimatedPositioned (inside Stack)
AnimatedPositioned(
  duration: Duration(milliseconds: 300),
  left: isLeft ? 0 : 100,
  top: isTop ? 0 : 100,
  child: widget,
)

// AnimatedSwitcher - Cross-fade between widgets
AnimatedSwitcher(
  duration: Duration(milliseconds: 300),
  transitionBuilder: (child, animation) {
    return FadeTransition(opacity: animation, child: child);
  },
  child: Text(
    currentText,
    key: ValueKey(currentText), // Important!
  ),
)

// TweenAnimationBuilder - Custom implicit animation
TweenAnimationBuilder<double>(
  tween: Tween(begin: 0, end: progress),
  duration: Duration(milliseconds: 500),
  builder: (context, value, child) {
    return CircularProgressIndicator(value: value);
  },
)
```

## 2. Explicit Animations

### AnimationController Pattern

```dart
class ExplicitAnimationWidget extends StatefulWidget {
  @override
  State<ExplicitAnimationWidget> createState() => _ExplicitAnimationWidgetState();
}

class _ExplicitAnimationWidgetState extends State<ExplicitAnimationWidget>
    with TickerProviderStateMixin {
  late final AnimationController _controller;
  late final Animation<Offset> _slideAnimation;
  late final Animation<double> _fadeAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Duration(milliseconds: 500),
      vsync: this,
    );

    _slideAnimation = Tween<Offset>(
      begin: Offset(0, 1),
      end: Offset.zero,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: Interval(0.0, 0.6, curve: Curves.easeOut),
    ));

    _fadeAnimation = Tween<double>(
      begin: 0,
      end: 1,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: Interval(0.3, 1.0, curve: Curves.easeIn),
    ));

    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SlideTransition(
      position: _slideAnimation,
      child: FadeTransition(
        opacity: _fadeAnimation,
        child: Content(),
      ),
    );
  }
}
```

### Animation Transitions

```dart
// Built-in transitions
FadeTransition(opacity: animation, child: widget)
SlideTransition(position: offsetAnimation, child: widget)
ScaleTransition(scale: animation, child: widget)
RotationTransition(turns: animation, child: widget)
SizeTransition(sizeFactor: animation, child: widget)

// AnimatedBuilder - Custom rendering
AnimatedBuilder(
  animation: _controller,
  builder: (context, child) {
    return Transform(
      transform: Matrix4.identity()
        ..setEntry(3, 2, 0.001)
        ..rotateY(_controller.value * pi),
      alignment: Alignment.center,
      child: child,
    );
  },
  child: Card(),
)
```

## 3. Hero Animations

```dart
// Source screen
Hero(
  tag: 'product-${product.id}',
  child: Image.network(product.imageUrl),
)

// Destination screen
Hero(
  tag: 'product-${product.id}',
  child: Image.network(product.imageUrl),
)

// Custom Hero flight
Hero(
  tag: 'avatar',
  flightShuttleBuilder: (
    flightContext,
    animation,
    flightDirection,
    fromHeroContext,
    toHeroContext,
  ) {
    return AnimatedBuilder(
      animation: animation,
      builder: (context, _) {
        return CircleAvatar(
          radius: lerpDouble(40, 60, animation.value),
        );
      },
    );
  },
  child: CircleAvatar(),
)
```

## 4. Staggered Animations

```dart
class StaggeredList extends StatefulWidget {
  @override
  State<StaggeredList> createState() => _StaggeredListState();
}

class _StaggeredListState extends State<StaggeredList>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  final List<Animation<Offset>> _animations = [];

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Duration(milliseconds: 1000),
      vsync: this,
    );

    // Create staggered animations
    for (int i = 0; i < 5; i++) {
      final start = i * 0.1;
      final end = start + 0.4;
      _animations.add(
        Tween<Offset>(begin: Offset(1, 0), end: Offset.zero).animate(
          CurvedAnimation(
            parent: _controller,
            curve: Interval(start, end, curve: Curves.easeOut),
          ),
        ),
      );
    }

    _controller.forward();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: List.generate(5, (index) {
        return SlideTransition(
          position: _animations[index],
          child: ListTile(title: Text('Item $index')),
        );
      }),
    );
  }
}
```

## 5. Physics-Based Animations

```dart
// Spring simulation
class SpringAnimation extends StatefulWidget {
  @override
  State<SpringAnimation> createState() => _SpringAnimationState();
}

class _SpringAnimationState extends State<SpringAnimation>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late Animation<double> _animation;

  final SpringDescription spring = SpringDescription(
    mass: 1,
    stiffness: 100,
    damping: 10,
  );

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this);

    final simulation = SpringSimulation(spring, 0, 1, 0);
    _controller.animateWith(simulation);

    _animation = _controller.drive(Tween(begin: 0.0, end: 100.0));
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _animation,
      builder: (context, child) {
        return Transform.translate(
          offset: Offset(0, _animation.value),
          child: child,
        );
      },
      child: Ball(),
    );
  }
}
```

## 6. Lottie & Rive Integration

```dart
// Lottie animation
import 'package:lottie/lottie.dart';

Lottie.asset(
  'assets/loading.json',
  width: 200,
  height: 200,
  fit: BoxFit.contain,
  repeat: true,
  animate: true,
  onLoaded: (composition) {
    _controller.duration = composition.duration;
  },
)

// Rive animation
import 'package:rive/rive.dart';

RiveAnimation.asset(
  'assets/animation.riv',
  fit: BoxFit.cover,
  stateMachines: ['StateMachine1'],
  onInit: (artboard) {
    final controller = StateMachineController.fromArtboard(
      artboard,
      'StateMachine1',
    );
    artboard.addController(controller!);
    _trigger = controller.findInput<bool>('trigger') as SMITrigger;
  },
)
```

## 7. Page Transitions

```dart
// Custom page route
class FadePageRoute<T> extends PageRouteBuilder<T> {
  final Widget page;

  FadePageRoute({required this.page})
      : super(
          pageBuilder: (context, animation, secondaryAnimation) => page,
          transitionsBuilder: (context, animation, secondaryAnimation, child) {
            return FadeTransition(opacity: animation, child: child);
          },
          transitionDuration: Duration(milliseconds: 300),
        );
}

// Slide + fade combined
transitionsBuilder: (context, animation, secondaryAnimation, child) {
  final offsetAnimation = Tween<Offset>(
    begin: Offset(1.0, 0.0),
    end: Offset.zero,
  ).animate(CurvedAnimation(
    parent: animation,
    curve: Curves.easeInOut,
  ));

  return SlideTransition(
    position: offsetAnimation,
    child: FadeTransition(
      opacity: animation,
      child: child,
    ),
  );
}
```

## 8. Performance Optimization

```dart
// Use const where possible
const AnimatedContainer(...)

// RepaintBoundary for expensive animations
RepaintBoundary(
  child: AnimatedWidget(),
)

// AnimatedBuilder isolates rebuilds
AnimatedBuilder(
  animation: _controller,
  child: ExpensiveWidget(), // Not rebuilt
  builder: (context, child) {
    return Transform.scale(
      scale: _controller.value,
      child: child, // Reused
    );
  },
)

// Avoid layout-triggering animations
// Good: Transform, Opacity
// Avoid: width/height in tight loops
```

## Troubleshooting Guide

**Issue: Animation jank (dropped frames)**
```
1. Use RepaintBoundary to isolate
2. Profile with DevTools Performance
3. Avoid layout changes during animation
4. Use AnimatedBuilder, not setState
5. Check for heavy build methods
```

**Issue: Animation doesn't start**
```
1. Verify AnimationController.forward() called
2. Check vsync: this (TickerProviderStateMixin)
3. Verify widget is mounted before animating
4. Check duration is set
```

**Issue: Animation leaks memory**
```
1. Dispose AnimationController in dispose()
2. Cancel any listeners
3. Use mounted check before setState
```

## Animation Selection Guide

| Need | Solution |
|------|----------|
| Simple property change | AnimatedContainer |
| Cross-fade widgets | AnimatedSwitcher |
| Custom timing control | AnimationController |
| Shared element | Hero |
| List items appearing | Staggered animations |
| Natural motion | Physics simulation |
| Complex vector | Lottie/Rive |

---

**Create fluid, 60fps animations in Flutter.**
