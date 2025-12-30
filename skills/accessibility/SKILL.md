---
name: accessibility
description: Flutter accessibility features and screen reader support
sasmp_version: "2.0.0"
eqhm_version: "1.1.0"
bonded_agent: 06-testing-qa
bond_type: PRIMARY_BOND
---

# Flutter Accessibility Skill

## Overview
Build inclusive Flutter apps with proper accessibility support for users with disabilities. Implement WCAG 2.1 compliance, screen reader support, and comprehensive a11y testing.

## Topics Covered

### Semantics
- Semantics widget
- Semantic labels
- Semantic properties
- MergeSemantics
- ExcludeSemantics

### Screen Readers
- TalkBack (Android)
- VoiceOver (iOS)
- Accessibility tree
- Focus management
- Announcements

### Visual Accessibility
- Color contrast
- Text scaling
- High contrast mode
- Reduced motion
- Large touch targets

### Keyboard Navigation
- Focus order
- Focus traversal
- Shortcut support
- Tab navigation
- Focus highlights

### Testing
- Accessibility inspector
- Semantics debugger
- Screen reader testing
- Automated a11y tests
- Manual testing checklist

## Core Patterns

### 🔷 Semantic Labels

```dart
// Custom icon button with proper semantics
class AccessibleIconButton extends StatelessWidget {
  final IconData icon;
  final String semanticLabel;
  final VoidCallback onPressed;

  const AccessibleIconButton({
    super.key,
    required this.icon,
    required this.semanticLabel,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return Semantics(
      button: true,
      label: semanticLabel,
      child: InkWell(
        onTap: onPressed,
        customBorder: const CircleBorder(),
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Icon(icon),
        ),
      ),
    );
  }
}

// Image with accessibility
class AccessibleImage extends StatelessWidget {
  final String imageUrl;
  final String description;
  final bool isDecorative;

  const AccessibleImage({
    super.key,
    required this.imageUrl,
    required this.description,
    this.isDecorative = false,
  });

  @override
  Widget build(BuildContext context) {
    final image = Image.network(
      imageUrl,
      semanticLabel: isDecorative ? null : description,
    );

    if (isDecorative) {
      return ExcludeSemantics(child: image);
    }

    return Semantics(
      image: true,
      label: description,
      child: image,
    );
  }
}
```

### 🔶 Interactive Elements

```dart
// Accessible card with proper focus
class AccessibleProductCard extends StatelessWidget {
  final Product product;
  final VoidCallback onTap;

  const AccessibleProductCard({
    super.key,
    required this.product,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Semantics(
      button: true,
      label: '${product.name}, ${product.formattedPrice}. '
          '${product.inStock ? "In stock" : "Out of stock"}. '
          'Double tap to view details.',
      child: InkWell(
        onTap: onTap,
        child: Card(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Exclude decorative image from semantics
              ExcludeSemantics(
                child: Image.network(product.imageUrl),
              ),
              Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      product.name,
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    Text(product.formattedPrice),
                    if (!product.inStock)
                      const Text(
                        'Out of stock',
                        style: TextStyle(color: Colors.red),
                      ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// Accessible toggle switch
class AccessibleSwitch extends StatelessWidget {
  final bool value;
  final String label;
  final ValueChanged<bool> onChanged;

  const AccessibleSwitch({
    super.key,
    required this.value,
    required this.label,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return MergeSemantics(
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Expanded(
            child: Text(label),
          ),
          Switch(
            value: value,
            onChanged: onChanged,
          ),
        ],
      ),
    );
  }
}
```

### 🟢 Focus Management

```dart
// Focus management for forms
class AccessibleForm extends StatefulWidget {
  const AccessibleForm({super.key});

  @override
  State<AccessibleForm> createState() => _AccessibleFormState();
}

class _AccessibleFormState extends State<AccessibleForm> {
  final _formKey = GlobalKey<FormState>();
  final _nameFocus = FocusNode();
  final _emailFocus = FocusNode();
  final _passwordFocus = FocusNode();

  @override
  void dispose() {
    _nameFocus.dispose();
    _emailFocus.dispose();
    _passwordFocus.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: FocusTraversalGroup(
        policy: OrderedTraversalPolicy(),
        child: Column(
          children: [
            FocusTraversalOrder(
              order: const NumericFocusOrder(1),
              child: TextFormField(
                focusNode: _nameFocus,
                decoration: const InputDecoration(
                  labelText: 'Name',
                  hintText: 'Enter your full name',
                ),
                textInputAction: TextInputAction.next,
                onFieldSubmitted: (_) {
                  FocusScope.of(context).requestFocus(_emailFocus);
                },
              ),
            ),
            const SizedBox(height: 16),
            FocusTraversalOrder(
              order: const NumericFocusOrder(2),
              child: TextFormField(
                focusNode: _emailFocus,
                decoration: const InputDecoration(
                  labelText: 'Email',
                  hintText: 'Enter your email address',
                ),
                keyboardType: TextInputType.emailAddress,
                textInputAction: TextInputAction.next,
                onFieldSubmitted: (_) {
                  FocusScope.of(context).requestFocus(_passwordFocus);
                },
              ),
            ),
            const SizedBox(height: 16),
            FocusTraversalOrder(
              order: const NumericFocusOrder(3),
              child: TextFormField(
                focusNode: _passwordFocus,
                decoration: const InputDecoration(
                  labelText: 'Password',
                  hintText: 'Enter your password',
                ),
                obscureText: true,
                textInputAction: TextInputAction.done,
                onFieldSubmitted: (_) => _submit(),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _submit() {
    if (_formKey.currentState!.validate()) {
      // Submit form
    }
  }
}
```

### 🟣 Live Region Announcements

```dart
// Announce dynamic content changes
class LiveRegionExample extends StatefulWidget {
  const LiveRegionExample({super.key});

  @override
  State<LiveRegionExample> createState() => _LiveRegionExampleState();
}

class _LiveRegionExampleState extends State<LiveRegionExample> {
  int _cartCount = 0;

  void _addToCart() {
    setState(() => _cartCount++);

    // Announce to screen readers
    SemanticsService.announce(
      'Item added to cart. Cart now has $_cartCount items.',
      TextDirection.ltr,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Semantics(
          liveRegion: true,
          child: Text('Cart: $_cartCount items'),
        ),
        ElevatedButton(
          onPressed: _addToCart,
          child: const Text('Add to Cart'),
        ),
      ],
    );
  }
}

// Error announcement
void showAccessibleError(BuildContext context, String message) {
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(
      content: Semantics(
        liveRegion: true,
        child: Text(message),
      ),
    ),
  );

  // Also announce for screen readers
  SemanticsService.announce(
    'Error: $message',
    TextDirection.ltr,
  );
}
```

### 🔴 Color Contrast & Visual

```dart
// Contrast-safe color extension
extension ContrastColor on Color {
  Color get contrastingTextColor {
    final luminance = computeLuminance();
    return luminance > 0.5 ? Colors.black : Colors.white;
  }

  bool meetsContrastRatio(Color background, {double minRatio = 4.5}) {
    final foregroundLuminance = computeLuminance();
    final backgroundLuminance = background.computeLuminance();

    final lighter = foregroundLuminance > backgroundLuminance
        ? foregroundLuminance
        : backgroundLuminance;
    final darker = foregroundLuminance > backgroundLuminance
        ? backgroundLuminance
        : foregroundLuminance;

    final ratio = (lighter + 0.05) / (darker + 0.05);
    return ratio >= minRatio;
  }
}

// Text scaling support
class ScalableText extends StatelessWidget {
  final String text;
  final TextStyle? style;
  final double maxScaleFactor;

  const ScalableText(
    this.text, {
    super.key,
    this.style,
    this.maxScaleFactor = 2.0,
  });

  @override
  Widget build(BuildContext context) {
    final mediaQuery = MediaQuery.of(context);
    final scaleFactor = mediaQuery.textScaler.clamp(
      minScaleFactor: 1.0,
      maxScaleFactor: maxScaleFactor,
    );

    return MediaQuery(
      data: mediaQuery.copyWith(textScaler: scaleFactor),
      child: Text(text, style: style),
    );
  }
}

// Reduced motion support
class ReducedMotionBuilder extends StatelessWidget {
  final Widget Function(BuildContext, bool) builder;

  const ReducedMotionBuilder({super.key, required this.builder});

  @override
  Widget build(BuildContext context) {
    final reduceMotion = MediaQuery.of(context).disableAnimations;
    return builder(context, reduceMotion);
  }
}

// Usage
ReducedMotionBuilder(
  builder: (context, reduceMotion) {
    return AnimatedContainer(
      duration: reduceMotion
          ? Duration.zero
          : const Duration(milliseconds: 300),
      // ...
    );
  },
)
```

### 🟠 Minimum Touch Targets

```dart
// Ensure 48x48 minimum touch target
class AccessibleTouchTarget extends StatelessWidget {
  final Widget child;
  final VoidCallback onTap;
  final String semanticLabel;

  const AccessibleTouchTarget({
    super.key,
    required this.child,
    required this.onTap,
    required this.semanticLabel,
  });

  @override
  Widget build(BuildContext context) {
    return Semantics(
      button: true,
      label: semanticLabel,
      child: InkWell(
        onTap: onTap,
        child: ConstrainedBox(
          constraints: const BoxConstraints(
            minWidth: 48,
            minHeight: 48,
          ),
          child: Center(child: child),
        ),
      ),
    );
  }
}

// Spacing between touch targets
class AccessibleButtonRow extends StatelessWidget {
  final List<Widget> buttons;

  const AccessibleButtonRow({super.key, required this.buttons});

  @override
  Widget build(BuildContext context) {
    return Wrap(
      spacing: 8, // Minimum 8dp between targets
      runSpacing: 8,
      children: buttons,
    );
  }
}
```

### 🔵 Custom Semantics Actions

```dart
class SwipeableCard extends StatelessWidget {
  final String title;
  final VoidCallback onDelete;
  final VoidCallback onArchive;

  const SwipeableCard({
    super.key,
    required this.title,
    required this.onDelete,
    required this.onArchive,
  });

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: title,
      customSemanticsActions: {
        CustomSemanticsAction(label: 'Delete'): onDelete,
        CustomSemanticsAction(label: 'Archive'): onArchive,
      },
      child: Dismissible(
        key: ValueKey(title),
        background: Container(color: Colors.red),
        secondaryBackground: Container(color: Colors.blue),
        onDismissed: (direction) {
          if (direction == DismissDirection.startToEnd) {
            onDelete();
          } else {
            onArchive();
          }
        },
        child: ListTile(title: Text(title)),
      ),
    );
  }
}
```

## Testing Patterns

### Semantic Testing

```dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('button has correct semantic label', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: IconButton(
            icon: const Icon(Icons.add),
            onPressed: () {},
            tooltip: 'Add item',
          ),
        ),
      ),
    );

    final semantics = tester.getSemantics(find.byType(IconButton));
    expect(semantics.label, 'Add item');
    expect(semantics.hasAction(SemanticsAction.tap), isTrue);
  });

  testWidgets('form fields have proper focus order', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: AccessibleForm()));

    // Verify focus traversal order
    final nameField = find.widgetWithText(TextFormField, 'Name');
    final emailField = find.widgetWithText(TextFormField, 'Email');

    await tester.tap(nameField);
    await tester.pump();

    // Tab to next field
    await tester.sendKeyEvent(LogicalKeyboardKey.tab);
    await tester.pump();

    expect(
      FocusScope.of(tester.element(emailField)).hasFocus,
      isTrue,
    );
  });

  testWidgets('image has semantic description', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Image.network(
          'https://example.com/image.jpg',
          semanticLabel: 'Product photo showing red shoes',
        ),
      ),
    );

    final semantics = tester.getSemantics(find.byType(Image));
    expect(semantics.label, 'Product photo showing red shoes');
  });
}
```

### Contrast Testing

```dart
void checkContrast(Color foreground, Color background) {
  final ratio = _calculateContrastRatio(foreground, background);

  // WCAG AA requires 4.5:1 for normal text
  expect(ratio, greaterThanOrEqualTo(4.5),
      reason: 'Text contrast ratio must be at least 4.5:1');

  // WCAG AAA requires 7:1
  // expect(ratio, greaterThanOrEqualTo(7.0));
}

double _calculateContrastRatio(Color foreground, Color background) {
  final fgLuminance = foreground.computeLuminance();
  final bgLuminance = background.computeLuminance();

  final lighter = fgLuminance > bgLuminance ? fgLuminance : bgLuminance;
  final darker = fgLuminance > bgLuminance ? bgLuminance : fgLuminance;

  return (lighter + 0.05) / (darker + 0.05);
}
```

## Troubleshooting Guide

### Common Issues

#### 1. Screen Reader Not Reading Content
```
❌ Symptom: TalkBack/VoiceOver skips element

✅ Debug Checklist:
□ Add Semantics widget with label
□ Check excludeSemantics is not blocking
□ Verify element is not zero-sized
□ Use debugDumpSemantics() to inspect tree
□ Test with actual device, not emulator
```

#### 2. Focus Not Moving Correctly
```
❌ Symptom: Tab order is wrong or focus gets stuck

✅ Solutions:
1. Use FocusTraversalGroup with policy
2. Add FocusTraversalOrder for explicit ordering
3. Check for FocusScope blocking traversal
4. Dispose FocusNodes properly
```

#### 3. Poor Color Contrast
```
❌ Symptom: Text hard to read

✅ Solutions:
1. Use Material theme colors (built-in contrast)
2. Test with Accessibility Scanner
3. Check computeLuminance() ratios
4. Provide high contrast theme option
```

#### 4. Touch Targets Too Small
```
❌ Symptom: Hard to tap buttons

✅ Solutions:
1. Minimum 48x48 dp touch area
2. Use IconButton (includes padding)
3. Add InkWell with expanded hit test area
4. Increase padding around tappable content
```

## Debug Commands

```bash
# Enable semantics debugger
flutter run --enable-software-rendering

# Dump semantics tree
# In app:
debugDumpSemantics()

# Test with TalkBack (Android)
adb shell settings put secure enabled_accessibility_services com.google.android.marvin.talkback/com.google.android.marvin.talkback.TalkBackService

# Disable TalkBack
adb shell settings put secure enabled_accessibility_services ""
```

## WCAG 2.1 Quick Reference

| Criterion | Level | Requirement |
|-----------|-------|-------------|
| 1.1.1 Non-text Content | A | Alt text for images |
| 1.4.3 Contrast (Minimum) | AA | 4.5:1 for text |
| 1.4.11 Non-text Contrast | AA | 3:1 for UI components |
| 2.1.1 Keyboard | A | All functionality via keyboard |
| 2.4.3 Focus Order | A | Logical focus sequence |
| 2.4.7 Focus Visible | AA | Visible focus indicator |
| 2.5.5 Target Size | AAA | 44x44 CSS pixels minimum |

## Integration Points

| Agent | Integration |
|-------|-------------|
| 01-UI-Development | Accessible widgets |
| 05-Performance | No a11y performance impact |
| 06-Testing-QA | Accessibility testing |

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Semantic Coverage | 100% | Audit tool |
| Contrast Ratio | ≥4.5:1 | Color analyzer |
| Touch Targets | ≥48dp | Layout inspector |
| Focus Order | Logical | Manual test |

## Prerequisites
- Flutter widget basics
- Widget tree understanding
- Platform accessibility basics

## Learning Outcomes
- Add semantic labels
- Support screen readers
- Ensure proper contrast
- Test accessibility

## EQHM Compliance

- ✅ **Ethical**: Inclusive design for all users
- ✅ **Quality**: WCAG 2.1 AA compliance
- ✅ **Honest**: Clear accessibility status
- ✅ **Maintainable**: Reusable a11y patterns

---

*This skill ensures Flutter apps are accessible to all users.*
