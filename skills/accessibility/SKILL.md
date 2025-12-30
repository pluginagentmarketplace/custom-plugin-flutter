---
name: custom-plugin-flutter-skill-accessibility
description: Production-grade Flutter accessibility mastery - Semantics API, screen readers (VoiceOver/TalkBack), WCAG 2.1 AA/AAA compliance, inclusive design patterns, automated a11y testing with comprehensive code examples
sasmp_version: "1.3.0"
bonded_agent: 06-testing-qa
bond_type: PRIMARY_BOND
---

# custom-plugin-flutter: Accessibility Skill

## Quick Start - Accessible Widget Pattern

```dart
class AccessibleProductCard extends StatelessWidget {
  final Product product;
  final VoidCallback onTap;
  final VoidCallback onAddToCart;

  const AccessibleProductCard({
    required this.product,
    required this.onTap,
    required this.onAddToCart,
  });

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: '${product.name}, ${product.formattedPrice}',
      hint: 'Double tap to view details',
      button: true,
      enabled: true,
      child: Card(
        child: InkWell(
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Image with semantic description
                Semantics(
                  image: true,
                  label: 'Product image: ${product.imageDescription}',
                  excludeSemantics: true,
                  child: Image.network(product.imageUrl, height: 120),
                ),
                const SizedBox(height: 12),
                Text(product.name),
                Text(product.formattedPrice),
                const SizedBox(height: 12),
                // 48dp minimum touch target
                ElevatedButton.icon(
                  onPressed: onAddToCart,
                  icon: const Icon(Icons.add_shopping_cart),
                  label: const Text('Add to Cart'),
                  style: ElevatedButton.styleFrom(
                    minimumSize: const Size(double.infinity, 48),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
```

## 1. Semantics Widget Deep Dive

### Core Semantic Properties

```dart
Semantics(
  // Identity
  label: 'Submit button',           // What this element IS
  value: '5 items',                  // Current value
  hint: 'Double tap to submit',     // How to interact

  // Traits
  button: true,
  link: false,
  header: false,
  image: false,
  textField: false,
  slider: false,

  // State
  enabled: true,
  checked: true,           // Checkbox state
  selected: false,
  toggled: false,
  focused: false,
  hidden: false,
  obscured: false,         // Password field

  // Actions
  onTap: () {},
  onLongPress: () {},
  onIncrease: () {},
  onDecrease: () {},
  onDismiss: () {},

  // Grouping
  container: false,
  explicitChildNodes: false,
  excludeSemantics: false,

  child: MyWidget(),
)
```

### Semantic Wrappers

```dart
// MergeSemantics - Combine into single node
MergeSemantics(
  child: Row(
    children: [
      Icon(Icons.star, semanticLabel: null),
      Text('4.5 stars'),
    ],
  ),
)
// Screen reader: "4.5 stars"

// ExcludeSemantics - Remove decorative elements
ExcludeSemantics(
  child: DecorativeBackground(),
)

// BlockSemantics - Block underlying content
BlockSemantics(
  child: ModalOverlay(),
)
```

## 2. Screen Reader Support

### VoiceOver (iOS) & TalkBack (Android)

```dart
// Custom sort order
Semantics(
  sortKey: OrdinalSortKey(1.0),
  child: FirstItem(),
)

// Announce changes dynamically
void announceChange(String message) {
  SemanticsService.announce(message, TextDirection.ltr);
}

// Live region for dynamic content
Semantics(
  liveRegion: true,
  child: CountdownTimer(),
)

// Custom actions
Semantics(
  customSemanticsActions: {
    CustomSemanticsAction(label: 'Mark as favorite'): markFavorite,
    CustomSemanticsAction(label: 'Share'): share,
  },
  child: ItemCard(),
)
```

## 3. Visual Accessibility

### Color Contrast (WCAG)

```dart
class ContrastChecker {
  // WCAG AA: 4.5:1 normal, 3:1 large text
  // WCAG AAA: 7:1 normal, 4.5:1 large text

  static double calculateContrast(Color fg, Color bg) {
    final fgL = fg.computeLuminance();
    final bgL = bg.computeLuminance();
    return (max(fgL, bgL) + 0.05) / (min(fgL, bgL) + 0.05);
  }

  static bool meetsAA(Color fg, Color bg, {bool largeText = false}) {
    return calculateContrast(fg, bg) >= (largeText ? 3.0 : 4.5);
  }
}
```

### Text Scaling & Reduced Motion

```dart
// Respect system text scale
final textScaler = MediaQuery.textScalerOf(context);

// Check reduced motion preference
final reduceMotion = MediaQuery.disableAnimationsOf(context);

if (reduceMotion) {
  return StaticWidget();
}
return AnimatedWidget(duration: Duration(milliseconds: 300));
```

## 4. Touch Targets & Keyboard Navigation

```dart
// Minimum 48x48 dp touch targets
ElevatedButton(
  onPressed: () {},
  child: Text('Tap'),
  style: ElevatedButton.styleFrom(
    minimumSize: Size(48, 48),
  ),
)

// Focus management
Focus(
  focusNode: _focusNode,
  onKeyEvent: (node, event) {
    if (event.logicalKey == LogicalKeyboardKey.enter) {
      handleAction();
      return KeyEventResult.handled;
    }
    return KeyEventResult.ignored;
  },
  child: MyWidget(),
)

// Custom focus order
FocusTraversalGroup(
  policy: OrderedTraversalPolicy(),
  child: Column(
    children: [
      FocusTraversalOrder(order: NumericFocusOrder(1), child: Field1()),
      FocusTraversalOrder(order: NumericFocusOrder(2), child: Field2()),
    ],
  ),
)
```

## 5. Testing Accessibility

```dart
testWidgets('meets accessibility guidelines', (tester) async {
  final semanticsHandle = tester.ensureSemantics();
  addTearDown(semanticsHandle.dispose);

  await tester.pumpWidget(MyApp());

  // Check semantic labels
  expect(find.bySemanticsLabel('Submit button'), findsOneWidget);

  // Check touch target size
  final button = tester.getSize(find.byType(ElevatedButton));
  expect(button.width, greaterThanOrEqualTo(48));
  expect(button.height, greaterThanOrEqualTo(48));

  // Verify semantics
  expect(tester.getSemantics(find.byType(MyButton)), matchesSemantics(
    label: 'Submit',
    isButton: true,
    isEnabled: true,
    hasTapAction: true,
  ));
});
```

## Troubleshooting Guide

**Issue: Screen reader skips element**
```
1. Check ExcludeSemantics wrapping
2. Verify semantic label exists
3. Check MergeSemantics parent
4. Run: flutter run --show-semantics-debug
```

**Issue: Wrong reading order**
```
1. Add OrdinalSortKey for custom order
2. Use FocusTraversalGroup
3. Check visual layout matches logical order
```

**Issue: Contrast too low**
```
1. Use ContrastChecker utility
2. Test light and dark themes
3. Check disabled state colors
```

## Manual Testing Checklist

```
[ ] All interactive elements have labels
[ ] Reading order is logical
[ ] Color contrast >= 4.5:1
[ ] Text scales to 200%
[ ] Touch targets >= 48dp
[ ] Keyboard navigation works
[ ] Focus indicators visible
```

---

**Build inclusive Flutter apps that everyone can use.**
