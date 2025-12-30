---
name: localization
description: Flutter internationalization and localization with intl
sasmp_version: "2.0.0"
eqhm_version: "1.1.0"
bonded_agent: 01-flutter-ui-development
bond_type: PRIMARY_BOND
---

# Flutter Localization Skill

## Overview
Implement internationalization (i18n) and localization (l10n) in Flutter apps for global audience support. Master ARB files, pluralization, and RTL layouts with production-grade patterns.

## Topics Covered

### Flutter Localization
- MaterialApp localization
- Localizations widget
- LocalizationsDelegate
- Locale resolution
- System locale detection

### intl Package
- ARB files
- Message extraction
- Pluralization
- Gender support
- Date/number formatting

### flutter_localizations
- Material localizations
- Cupertino localizations
- RTL support
- Calendar systems
- Number systems

### Code Generation
- intl_utils
- flutter gen-l10n
- slang package
- Easy localization
- Automated translation

### Best Practices
- String externalization
- Translation workflow
- Testing localization
- Dynamic locale switching
- Locale persistence

## Core Patterns

### 🔷 Project Setup

```yaml
# pubspec.yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_localizations:
    sdk: flutter
  intl: ^0.19.0

flutter:
  generate: true
```

```yaml
# l10n.yaml (project root)
arb-dir: lib/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
output-class: AppLocalizations
nullable-getter: false
```

### 🔶 ARB Files

```json
// lib/l10n/app_en.arb
{
  "@@locale": "en",
  "appTitle": "My App",
  "@appTitle": {
    "description": "The title of the application"
  },
  "welcomeMessage": "Welcome, {userName}!",
  "@welcomeMessage": {
    "description": "Welcome message with user name",
    "placeholders": {
      "userName": {
        "type": "String",
        "example": "John"
      }
    }
  },
  "itemCount": "{count, plural, =0{No items} =1{1 item} other{{count} items}}",
  "@itemCount": {
    "description": "Shows the number of items",
    "placeholders": {
      "count": {
        "type": "int"
      }
    }
  },
  "lastUpdated": "Last updated: {date}",
  "@lastUpdated": {
    "description": "Shows when content was last updated",
    "placeholders": {
      "date": {
        "type": "DateTime",
        "format": "yMMMd"
      }
    }
  },
  "price": "Price: {amount}",
  "@price": {
    "description": "Shows the price",
    "placeholders": {
      "amount": {
        "type": "double",
        "format": "currency",
        "optionalParameters": {
          "symbol": "$",
          "decimalDigits": 2
        }
      }
    }
  },
  "gender": "{gender, select, male{He} female{She} other{They}} liked this",
  "@gender": {
    "description": "Gender-specific message",
    "placeholders": {
      "gender": {
        "type": "String"
      }
    }
  }
}
```

```json
// lib/l10n/app_tr.arb
{
  "@@locale": "tr",
  "appTitle": "Uygulamam",
  "welcomeMessage": "Hoş geldin, {userName}!",
  "itemCount": "{count, plural, =0{Öğe yok} =1{1 öğe} other{{count} öğe}}",
  "lastUpdated": "Son güncelleme: {date}",
  "price": "Fiyat: {amount}",
  "gender": "{gender, select, male{O} female{O} other{Onlar}} bunu beğendi"
}
```

### 🟢 App Configuration

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  Locale _locale = const Locale('en');

  void setLocale(Locale locale) {
    setState(() => _locale = locale);
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Localized App',
      locale: _locale,
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: AppLocalizations.supportedLocales,
      localeResolutionCallback: (locale, supportedLocales) {
        // Check if the current device locale is supported
        for (final supportedLocale in supportedLocales) {
          if (supportedLocale.languageCode == locale?.languageCode) {
            return supportedLocale;
          }
        }
        // If not supported, return the first supported locale
        return supportedLocales.first;
      },
      home: const HomePage(),
    );
  }
}
```

### 🟣 Using Localizations

```dart
// lib/pages/home_page.dart
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.appTitle),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Simple string
            Text(l10n.welcomeMessage('John')),

            const SizedBox(height: 16),

            // Pluralization
            Text(l10n.itemCount(0)),  // "No items"
            Text(l10n.itemCount(1)),  // "1 item"
            Text(l10n.itemCount(5)),  // "5 items"

            const SizedBox(height: 16),

            // Date formatting
            Text(l10n.lastUpdated(DateTime.now())),

            const SizedBox(height: 16),

            // Currency formatting
            Text(l10n.price(29.99)),

            const SizedBox(height: 16),

            // Gender selection
            Text(l10n.gender('male')),   // "He liked this"
            Text(l10n.gender('female')), // "She liked this"
          ],
        ),
      ),
    );
  }
}

// Extension for easier access
extension LocalizationExtension on BuildContext {
  AppLocalizations get l10n => AppLocalizations.of(this);
}

// Usage with extension
class ExampleWidget extends StatelessWidget {
  const ExampleWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Text(context.l10n.appTitle);
  }
}
```

### 🔴 RTL Support

```dart
// Automatic RTL detection
class RTLAwareWidget extends StatelessWidget {
  const RTLAwareWidget({super.key});

  @override
  Widget build(BuildContext context) {
    final isRTL = Directionality.of(context) == TextDirection.rtl;

    return Row(
      children: [
        // Icons automatically flip for RTL
        Icon(isRTL ? Icons.arrow_back : Icons.arrow_forward),

        const SizedBox(width: 8),

        // Text follows text direction automatically
        const Expanded(
          child: Text('This text will flow correctly'),
        ),
      ],
    );
  }
}

// Manual directional widgets
class DirectionalPadding extends StatelessWidget {
  const DirectionalPadding({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      // Use EdgeInsetsDirectional for RTL-aware padding
      padding: const EdgeInsetsDirectional.only(start: 16, end: 8),
      child: Row(
        children: [
          // Use alignment constants that respect directionality
          const Align(
            alignment: AlignmentDirectional.centerStart,
            child: Text('Start aligned'),
          ),
        ],
      ),
    );
  }
}

// Force specific direction
class ForceDirection extends StatelessWidget {
  const ForceDirection({super.key});

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: TextDirection.ltr, // Force LTR for this subtree
      child: Row(
        children: const [
          Text('Always LTR'),
        ],
      ),
    );
  }
}
```

### 🟠 Locale Persistence

```dart
// lib/services/locale_service.dart
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LocaleService extends ChangeNotifier {
  static const _localeKey = 'app_locale';

  Locale _locale = const Locale('en');
  Locale get locale => _locale;

  LocaleService() {
    _loadLocale();
  }

  Future<void> _loadLocale() async {
    final prefs = await SharedPreferences.getInstance();
    final languageCode = prefs.getString(_localeKey);

    if (languageCode != null) {
      _locale = Locale(languageCode);
      notifyListeners();
    }
  }

  Future<void> setLocale(Locale locale) async {
    if (_locale == locale) return;

    _locale = locale;
    notifyListeners();

    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_localeKey, locale.languageCode);
  }
}

// With Riverpod
// final localeProvider = StateNotifierProvider<LocaleNotifier, Locale>((ref) {
//   return LocaleNotifier();
// });

// Language selector widget
class LanguageSelector extends StatelessWidget {
  const LanguageSelector({super.key});

  @override
  Widget build(BuildContext context) {
    return PopupMenuButton<Locale>(
      icon: const Icon(Icons.language),
      onSelected: (locale) {
        // Update app locale
        context.findAncestorStateOfType<_MyAppState>()?.setLocale(locale);
      },
      itemBuilder: (context) => const [
        PopupMenuItem(
          value: Locale('en'),
          child: Text('English'),
        ),
        PopupMenuItem(
          value: Locale('tr'),
          child: Text('Türkçe'),
        ),
        PopupMenuItem(
          value: Locale('ar'),
          child: Text('العربية'),
        ),
        PopupMenuItem(
          value: Locale('ja'),
          child: Text('日本語'),
        ),
      ],
    );
  }
}
```

### 🔵 Date & Number Formatting

```dart
import 'package:intl/intl.dart';

class FormattingExamples {
  // Date formatting
  String formatDate(DateTime date, String locale) {
    return DateFormat.yMMMEd(locale).format(date);
    // English: "Tue, Dec 31, 2024"
    // Turkish: "Sal, 31 Ara 2024"
  }

  String formatTime(DateTime time, String locale) {
    return DateFormat.jm(locale).format(time);
    // English: "2:30 PM"
    // Turkish: "14:30"
  }

  String formatRelativeDate(DateTime date, String locale) {
    final now = DateTime.now();
    final difference = now.difference(date);

    if (difference.inDays == 0) {
      return 'Today';
    } else if (difference.inDays == 1) {
      return 'Yesterday';
    } else if (difference.inDays < 7) {
      return DateFormat.EEEE(locale).format(date);
    } else {
      return DateFormat.yMd(locale).format(date);
    }
  }

  // Number formatting
  String formatNumber(num number, String locale) {
    return NumberFormat('#,##0.##', locale).format(number);
    // English: "1,234.56"
    // German: "1.234,56"
  }

  String formatCurrency(double amount, String locale, String currency) {
    return NumberFormat.currency(
      locale: locale,
      symbol: currency,
      decimalDigits: 2,
    ).format(amount);
    // US: "$1,234.56"
    // EU: "1.234,56 €"
  }

  String formatPercentage(double value, String locale) {
    return NumberFormat.percentPattern(locale).format(value);
    // 0.75 -> "75%"
  }

  String formatCompact(num number, String locale) {
    return NumberFormat.compact(locale: locale).format(number);
    // 1000 -> "1K"
    // 1500000 -> "1.5M"
  }
}
```

## Testing Localization

```dart
// test/localization_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

void main() {
  Widget createTestWidget({Locale locale = const Locale('en')}) {
    return MaterialApp(
      locale: locale,
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
      ],
      supportedLocales: AppLocalizations.supportedLocales,
      home: const TestPage(),
    );
  }

  group('Localization Tests', () {
    testWidgets('displays English text correctly', (tester) async {
      await tester.pumpWidget(createTestWidget(locale: const Locale('en')));
      await tester.pumpAndSettle();

      expect(find.text('My App'), findsOneWidget);
    });

    testWidgets('displays Turkish text correctly', (tester) async {
      await tester.pumpWidget(createTestWidget(locale: const Locale('tr')));
      await tester.pumpAndSettle();

      expect(find.text('Uygulamam'), findsOneWidget);
    });

    testWidgets('pluralization works correctly', (tester) async {
      await tester.pumpWidget(createTestWidget());
      await tester.pumpAndSettle();

      final l10n = AppLocalizations.of(
        tester.element(find.byType(TestPage)),
      );

      expect(l10n.itemCount(0), 'No items');
      expect(l10n.itemCount(1), '1 item');
      expect(l10n.itemCount(5), '5 items');
    });

    testWidgets('RTL layout is correct for Arabic', (tester) async {
      await tester.pumpWidget(createTestWidget(locale: const Locale('ar')));
      await tester.pumpAndSettle();

      final directionality = Directionality.of(
        tester.element(find.byType(TestPage)),
      );
      expect(directionality, TextDirection.rtl);
    });
  });
}

class TestPage extends StatelessWidget {
  const TestPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(AppLocalizations.of(context).appTitle),
      ),
    );
  }
}
```

## Troubleshooting Guide

### Common Issues

#### 1. Generated Files Not Found
```
❌ Error: Target of URI doesn't exist: 'package:flutter_gen/gen_l10n/app_localizations.dart'

✅ Solutions:
1. Add `generate: true` to pubspec.yaml flutter section
2. Create l10n.yaml in project root
3. Run `flutter pub get`
4. Run `flutter gen-l10n`
5. Restart IDE
```

#### 2. Missing Translation Key
```
❌ Error: The getter 'myKey' isn't defined for the type 'AppLocalizations'

✅ Debug Checklist:
□ Verify key exists in app_en.arb (template file)
□ Check for typos in key name
□ Run `flutter gen-l10n` again
□ Ensure @ metadata is valid JSON
```

#### 3. ARB Parsing Error
```
❌ Error: Could not parse ARB file

✅ Solutions:
1. Validate JSON syntax (use jsonlint)
2. Check for trailing commas
3. Ensure placeholders are correctly defined
4. Verify @key metadata format
```

#### 4. Locale Not Changing
```
❌ Symptom: App doesn't update when locale changes

✅ Solutions:
1. Wrap locale change in setState
2. Ensure MaterialApp rebuilds with new locale
3. Check localeResolutionCallback returns correct locale
4. Verify supportedLocales includes the locale
```

## Debug Commands

```bash
# Generate localizations
flutter gen-l10n

# Validate ARB files
flutter gen-l10n --no-synthetic-package

# List supported locales
flutter gen-l10n --help

# Check for unused translations
# Use intl_utils or similar tool
```

## Translation Workflow

```
1. Developer adds English string to app_en.arb
   ↓
2. Run flutter gen-l10n
   ↓
3. Export ARB files to translators
   ↓
4. Translators provide translated ARB files
   ↓
5. Import translated ARB files to lib/l10n/
   ↓
6. Run flutter gen-l10n again
   ↓
7. Test all locales
```

## Integration Points

| Agent | Integration |
|-------|-------------|
| 01-UI-Development | Localized UI strings |
| 06-Testing-QA | Localization testing |
| 07-DevOps | Translation CI/CD |

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Translation Coverage | 100% | ARB comparison |
| RTL Support | Full | Manual testing |
| Date/Number Format | Correct | Unit tests |
| Locale Persistence | Works | Integration test |

## Prerequisites
- Flutter widget basics
- State management
- ARB file format

## Learning Outcomes
- Set up localization
- Support multiple languages
- Handle RTL layouts
- Format dates/numbers

## EQHM Compliance

- ✅ **Ethical**: Inclusive global access
- ✅ **Quality**: Complete translation coverage
- ✅ **Honest**: Clear language options
- ✅ **Maintainable**: ARB-based workflow

---

*This skill enables global reach through proper localization.*
