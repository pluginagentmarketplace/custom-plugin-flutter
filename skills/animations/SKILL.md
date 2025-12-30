---
name: animations
description: Flutter animations from implicit to custom animations
sasmp_version: "2.0.0"
eqhm_version: "1.1.0"
bonded_agent: 01-flutter-ui-development
bond_type: PRIMARY_BOND
---

# Flutter Animations Skill

## Overview
Create fluid, performant animations in Flutter from simple implicit animations to complex custom animation sequences. Master 60fps animations with production-grade patterns.

## Topics Covered

### Implicit Animations
- AnimatedContainer
- AnimatedOpacity
- AnimatedPositioned
- AnimatedDefaultTextStyle
- TweenAnimationBuilder

### Explicit Animations
- AnimationController
- Tween and CurvedAnimation
- AnimatedBuilder
- AnimatedWidget
- Animation listeners

### Complex Animations
- Staggered animations
- Hero animations
- Page transitions
- Physics-based animations
- Custom painters with animation

### Animation Patterns
- Lottie integration
- Rive animations
- Particle effects
- Morphing animations
- Loading animations

### Performance
- Animation performance tips
- RepaintBoundary usage
- AnimatedBuilder optimization
- Avoiding jank
- 60fps maintenance

## Core Patterns

### 🔷 Implicit Animation Example

```dart
// Simple state-driven animation
class AnimatedCard extends StatefulWidget {
  const AnimatedCard({super.key});

  @override
  State<AnimatedCard> createState() => _AnimatedCardState();
}

class _AnimatedCardState extends State<AnimatedCard> {
  bool _isExpanded = false;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => setState(() => _isExpanded = !_isExpanded),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOutCubic,
        width: _isExpanded ? 300 : 150,
        height: _isExpanded ? 200 : 100,
        decoration: BoxDecoration(
          color: _isExpanded ? Colors.blue : Colors.grey,
          borderRadius: BorderRadius.circular(_isExpanded ? 16 : 8),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(_isExpanded ? 0.3 : 0.1),
              blurRadius: _isExpanded ? 20 : 5,
              offset: Offset(0, _isExpanded ? 10 : 2),
            ),
          ],
        ),
        child: AnimatedOpacity(
          duration: const Duration(milliseconds: 200),
          opacity: _isExpanded ? 1.0 : 0.7,
          child: const Center(
            child: Text('Tap me', style: TextStyle(color: Colors.white)),
          ),
        ),
      ),
    );
  }
}
```

### 🔶 Explicit Animation with Controller

```dart
class PulseAnimation extends StatefulWidget {
  final Widget child;
  const PulseAnimation({super.key, required this.child});

  @override
  State<PulseAnimation> createState() => _PulseAnimationState();
}

class _PulseAnimationState extends State<PulseAnimation>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final Animation<double> _scaleAnimation;
  late final Animation<double> _opacityAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    )..repeat(reverse: true);

    _scaleAnimation = Tween<double>(begin: 1.0, end: 1.1).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );

    _opacityAnimation = Tween<double>(begin: 0.7, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
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
      child: widget.child,
    );
  }
}
```

### 🟢 Staggered Animation

```dart
class StaggeredListAnimation extends StatefulWidget {
  final List<Widget> children;
  const StaggeredListAnimation({super.key, required this.children});

  @override
  State<StaggeredListAnimation> createState() => _StaggeredListAnimationState();
}

class _StaggeredListAnimationState extends State<StaggeredListAnimation>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final List<Animation<Offset>> _slideAnimations;
  late final List<Animation<double>> _fadeAnimations;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Duration(milliseconds: 300 * widget.children.length),
      vsync: this,
    );

    _slideAnimations = List.generate(widget.children.length, (index) {
      final start = index / widget.children.length;
      final end = (index + 1) / widget.children.length;
      return Tween<Offset>(
        begin: const Offset(0, 0.5),
        end: Offset.zero,
      ).animate(
        CurvedAnimation(
          parent: _controller,
          curve: Interval(start, end, curve: Curves.easeOutCubic),
        ),
      );
    });

    _fadeAnimations = List.generate(widget.children.length, (index) {
      final start = index / widget.children.length;
      final end = (index + 1) / widget.children.length;
      return Tween<double>(begin: 0, end: 1).animate(
        CurvedAnimation(
          parent: _controller,
          curve: Interval(start, end, curve: Curves.easeOut),
        ),
      );
    });

    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: List.generate(widget.children.length, (index) {
        return SlideTransition(
          position: _slideAnimations[index],
          child: FadeTransition(
            opacity: _fadeAnimations[index],
            child: widget.children[index],
          ),
        );
      }),
    );
  }
}
```

### 🟣 Hero Animation with Custom Flight

```dart
// Source page
Hero(
  tag: 'product-${product.id}',
  flightShuttleBuilder: (
    BuildContext context,
    Animation<double> animation,
    HeroFlightDirection direction,
    BuildContext fromContext,
    BuildContext toContext,
  ) {
    return AnimatedBuilder(
      animation: animation,
      builder: (context, child) {
        return Material(
          color: Colors.transparent,
          child: Transform.scale(
            scale: 1 + (0.1 * Curves.easeInOut.transform(
              direction == HeroFlightDirection.push
                  ? animation.value
                  : 1 - animation.value,
            )),
            child: child,
          ),
        );
      },
      child: Image.network(product.imageUrl, fit: BoxFit.cover),
    );
  },
  child: Image.network(product.imageUrl, fit: BoxFit.cover),
)

// Custom page route with Hero
class HeroPageRoute<T> extends PageRouteBuilder<T> {
  final Widget page;

  HeroPageRoute({required this.page})
      : super(
          pageBuilder: (context, animation, secondaryAnimation) => page,
          transitionsBuilder: (context, animation, secondaryAnimation, child) {
            return FadeTransition(
              opacity: animation,
              child: child,
            );
          },
          transitionDuration: const Duration(milliseconds: 400),
        );
}
```

### 🔴 Physics-Based Animation

```dart
class SpringAnimation extends StatefulWidget {
  const SpringAnimation({super.key});

  @override
  State<SpringAnimation> createState() => _SpringAnimationState();
}

class _SpringAnimationState extends State<SpringAnimation>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late Animation<double> _animation;
  double _dragStartY = 0;
  double _currentY = 0;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this);
  }

  void _onPanStart(DragStartDetails details) {
    _controller.stop();
    _dragStartY = details.localPosition.dy;
  }

  void _onPanUpdate(DragUpdateDetails details) {
    setState(() {
      _currentY = details.localPosition.dy - _dragStartY;
    });
  }

  void _onPanEnd(DragEndDetails details) {
    final velocity = details.velocity.pixelsPerSecond.dy;

    _animation = _controller.drive(
      Tween<double>(begin: _currentY, end: 0),
    );

    const spring = SpringDescription(
      mass: 1,
      stiffness: 300,
      damping: 20,
    );

    final simulation = SpringSimulation(spring, _currentY, 0, velocity / 1000);
    _controller.animateWith(simulation);

    _animation.addListener(() {
      setState(() {
        _currentY = _animation.value;
      });
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onPanStart: _onPanStart,
      onPanUpdate: _onPanUpdate,
      onPanEnd: _onPanEnd,
      child: Transform.translate(
        offset: Offset(0, _currentY),
        child: Container(
          width: 100,
          height: 100,
          decoration: const BoxDecoration(
            color: Colors.blue,
            shape: BoxShape.circle,
          ),
        ),
      ),
    );
  }
}
```

### 🟠 Lottie Integration

```dart
// pubspec.yaml
// dependencies:
//   lottie: ^2.7.0

class LottieAnimationWidget extends StatefulWidget {
  final String assetPath;
  final bool autoPlay;
  final bool loop;

  const LottieAnimationWidget({
    super.key,
    required this.assetPath,
    this.autoPlay = true,
    this.loop = true,
  });

  @override
  State<LottieAnimationWidget> createState() => _LottieAnimationWidgetState();
}

class _LottieAnimationWidgetState extends State<LottieAnimationWidget>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Lottie.asset(
      widget.assetPath,
      controller: _controller,
      onLoaded: (composition) {
        _controller.duration = composition.duration;
        if (widget.autoPlay) {
          widget.loop ? _controller.repeat() : _controller.forward();
        }
      },
    );
  }

  void play() => _controller.forward();
  void pause() => _controller.stop();
  void reset() => _controller.reset();
}
```

## Performance Optimization

### RepaintBoundary Usage

```dart
// Isolate animations from static content
class OptimizedAnimatedList extends StatelessWidget {
  final List<AnimatedItem> items;

  const OptimizedAnimatedList({super.key, required this.items});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: items.length,
      itemBuilder: (context, index) {
        return RepaintBoundary(
          child: AnimatedListItem(item: items[index]),
        );
      },
    );
  }
}
```

### Use AnimatedBuilder Correctly

```dart
// ✅ CORRECT: Child is cached
AnimatedBuilder(
  animation: _controller,
  builder: (context, child) {
    return Transform.rotate(
      angle: _controller.value * 2 * pi,
      child: child, // Reused, not rebuilt
    );
  },
  child: ExpensiveWidget(), // Built once
)

// ❌ WRONG: Child rebuilt every frame
AnimatedBuilder(
  animation: _controller,
  builder: (context, child) {
    return Transform.rotate(
      angle: _controller.value * 2 * pi,
      child: ExpensiveWidget(), // Rebuilt 60 times/second!
    );
  },
)
```

## Troubleshooting Guide

### Common Issues

#### 1. Animation Jank
```
❌ Symptom: Animation stutters or drops frames

✅ Solutions:
1. Wrap animated widgets in RepaintBoundary
2. Avoid expensive builds in animation callbacks
3. Use AnimatedBuilder with cached child
4. Check for layout thrashing
5. Profile with DevTools Performance tab
```

#### 2. Controller Disposed Error
```
❌ Error: AnimationController disposed after use

✅ Solutions:
1. Check mounted before setState in callbacks
2. Cancel animation listeners in dispose()
3. Use animation.removeStatusListener()
4. Null check controller before use
```

#### 3. Hero Animation Not Working
```
❌ Symptom: No hero animation between routes

✅ Debug Checklist:
□ Verify tag matches exactly on both routes
□ Ensure hero is visible on both pages
□ Check for opacity = 0 issues
□ Wrap in Material for proper rendering
```

#### 4. Infinite Animation Memory Leak
```
❌ Symptom: Memory grows with repeating animation

✅ Solutions:
1. Always dispose controller in dispose()
2. Use TickerProviderStateMixin correctly
3. Avoid creating new animations in build()
```

## Debug Commands

```bash
# Profile animation performance
flutter run --profile

# Enable performance overlay
# In app: MaterialApp(showPerformanceOverlay: true)

# Check for shader compilation jank
flutter run --profile --cache-sksl
```

## Integration Points

| Agent | Integration |
|-------|-------------|
| 01-UI-Development | Animation in widgets |
| 05-Performance | 60fps optimization |
| 06-Testing-QA | Animation testing |

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Frame Rate | 60fps | DevTools |
| Jank Frames | <1% | Performance overlay |
| Memory Stable | No leaks | Memory profiler |
| Animation Duration | <400ms | UX standard |

## Prerequisites
- Flutter widget basics
- State management
- Custom painters

## Learning Outcomes
- Create smooth animations
- Implement hero transitions
- Build loading animations
- Optimize animation performance

## EQHM Compliance

- ✅ **Ethical**: Respect reduced motion preferences
- ✅ **Quality**: 60fps smooth animations
- ✅ **Honest**: Clear performance expectations
- ✅ **Maintainable**: Reusable animation patterns

---

*This skill creates polished, performant Flutter animations.*
