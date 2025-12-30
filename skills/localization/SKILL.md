---
name: custom-plugin-flutter-skill-localization
description: Production-grade Flutter localization mastery - ARB files, flutter_localizations, intl package, pluralization, RTL support, dynamic locale switching with comprehensive code examples
sasmp_version: "1.3.0"
bonded_agent: 01-flutter-ui-development
bond_type: PRIMARY_BOND
---

# custom-plugin-flutter: Localization Skill

## Quick Start - Production Localization Setup

```yaml
# pubspec.yaml
dependencies:
  flutter_localizations:
    sdk: flutter
  intl: ^0.19.0

flutter:
  generate: true

# l10n.yaml (create in project root)
arb-dir: lib/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
output-class: AppLocalizations
nullable-getter: false
```

```dart
// lib/l10n/app_en.arb
{
  "@@locale": "en",
  "appTitle": "My App",
  "@appTitle": {
    "description": "The app title"
  },
  "welcomeMessage": "Welcome, {name}!",
  "@welcomeMessage": {
    "description": "Welcome message with user name",
    "placeholders": {
      "name": {
        "type": "String",
        "example": "John"
      }
    }
  },
  "itemCount": "{count, plural, =0{No items} =1{1 item} other{{count} items}}",
  "@itemCount": {
    "description": "Number of items",
    "placeholders": {
      "count": {
        "type": "int"
      }
    }
  }
}

// lib/l10n/app_tr.arb
{
  "@@locale": "tr",
  "appTitle": "Uygulamam",
  "welcomeMessage": "Hoş geldin, {name}!",
  "itemCount": "{count, plural, =0{Öğe yok} =1{1 öğe} other{{count} öğe}}"
}

// main.dart
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      localizationsDelegates: AppLocalizations.localizationsDelegates,
      supportedLocales: AppLocalizations.supportedLocales,
      locale: Locale('en'),
      home: HomePage(),
    );
  }
}

// Usage in widgets
Text(AppLocalizations.of(context).welcomeMessage('John'))
Text(AppLocalizations.of(context).itemCount(5))
```

## 1. ARB File Syntax

### Basic Messages

```json
{
  "@@locale": "en",

  "greeting": "Hello",
  "@greeting": {
    "description": "A simple greeting"
  },

  "pageTitle": "Settings Page",
  "@pageTitle": {
    "description": "Title of the settings page",
    "context": "SettingsPage"
  }
}
```

### Placeholders

```json
{
  "welcomeUser": "Welcome, {userName}!",
  "@welcomeUser": {
    "placeholders": {
      "userName": {
        "type": "String",
        "example": "Alice"
      }
    }
  },

  "priceLabel": "Price: {price}",
  "@priceLabel": {
    "placeholders": {
      "price": {
        "type": "double",
        "format": "currency",
        "optionalParameters": {
          "symbol": "$",
          "decimalDigits": 2
        }
      }
    }
  },

  "dateLabel": "Date: {date}",
  "@dateLabel": {
    "placeholders": {
      "date": {
        "type": "DateTime",
        "format": "yMMMd"
      }
    }
  }
}
```

### Pluralization

```json
{
  "cartItems": "{count, plural, =0{Your cart is empty} =1{1 item in cart} other{{count} items in cart}}",
  "@cartItems": {
    "placeholders": {
      "count": {
        "type": "int"
      }
    }
  },

  "remainingAttempts": "{count, plural, =0{No attempts remaining} =1{1 attempt remaining} other{{count} attempts remaining}}",
  "@remainingAttempts": {
    "placeholders": {
      "count": {
        "type": "int"
      }
    }
  }
}
```

### Gender Selection

```json
{
  "userGreeting": "{gender, select, male{Mr. {name}} female{Ms. {name}} other{{name}}}",
  "@userGreeting": {
    "placeholders": {
      "gender": {
        "type": "String"
      },
      "name": {
        "type": "String"
      }
    }
  }
}
```

## 2. Date & Number Formatting

```dart
import 'package:intl/intl.dart';

// Date formatting
final dateFormatter = DateFormat.yMMMd(locale);
Text(dateFormatter.format(DateTime.now()))

// Number formatting
final numberFormatter = NumberFormat.decimalPattern(locale);
Text(numberFormatter.format(1234567.89))

// Currency formatting
final currencyFormatter = NumberFormat.currency(
  locale: locale,
  symbol: '\$',
  decimalDigits: 2,
);
Text(currencyFormatter.format(99.99))

// Percentage
final percentFormatter = NumberFormat.percentPattern(locale);
Text(percentFormatter.format(0.75)) // 75%

// Compact notation
final compactFormatter = NumberFormat.compact(locale: locale);
Text(compactFormatter.format(1500000)) // 1.5M
```

## 3. Dynamic Locale Switching

```dart
class LocaleProvider extends ChangeNotifier {
  Locale _locale = Locale('en');

  Locale get locale => _locale;

  void setLocale(Locale locale) {
    if (!AppLocalizations.supportedLocales.contains(locale)) return;
    _locale = locale;
    notifyListeners();
  }

  Future<void> loadSavedLocale() async {
    final prefs = await SharedPreferences.getInstance();
    final languageCode = prefs.getString('languageCode');
    if (languageCode != null) {
      _locale = Locale(languageCode);
      notifyListeners();
    }
  }

  Future<void> saveLocale(Locale locale) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('languageCode', locale.languageCode);
    setLocale(locale);
  }
}

// Usage with Provider
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<LocaleProvider>(
      builder: (context, localeProvider, child) {
        return MaterialApp(
          locale: localeProvider.locale,
          localizationsDelegates: AppLocalizations.localizationsDelegates,
          supportedLocales: AppLocalizations.supportedLocales,
          home: HomePage(),
        );
      },
    );
  }
}

// Language selector
class LanguageSelector extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final localeProvider = context.watch<LocaleProvider>();

    return DropdownButton<Locale>(
      value: localeProvider.locale,
      items: AppLocalizations.supportedLocales.map((locale) {
        return DropdownMenuItem(
          value: locale,
          child: Text(_getLanguageName(locale)),
        );
      }).toList(),
      onChanged: (locale) {
        if (locale != null) {
          localeProvider.saveLocale(locale);
        }
      },
    );
  }

  String _getLanguageName(Locale locale) {
    switch (locale.languageCode) {
      case 'en': return 'English';
      case 'tr': return 'Türkçe';
      case 'es': return 'Español';
      default: return locale.languageCode;
    }
  }
}
```

## 4. RTL (Right-to-Left) Support

```dart
// Automatic direction based on locale
MaterialApp(
  locale: Locale('ar'), // Arabic - RTL
  localizationsDelegates: [
    GlobalMaterialLocalizations.delegate,
    GlobalWidgetsLocalizations.delegate,
    GlobalCupertinoLocalizations.delegate,
  ],
)

// Check directionality
final isRtl = Directionality.of(context) == TextDirection.rtl;

// Force direction
Directionality(
  textDirection: TextDirection.rtl,
  child: MyWidget(),
)

// Directional padding
Padding(
  padding: EdgeInsetsDirectional.only(start: 16, end: 8),
  child: Text('Directional padding'),
)

// Positioned directionally
PositionedDirectional(
  start: 0,
  end: null,
  child: widget,
)

// Row with automatic alignment
Row(
  textDirection: Directionality.of(context),
  children: [...],
)

// Icons that should flip
Transform.flip(
  flipX: isRtl,
  child: Icon(Icons.arrow_forward),
)
```

## 5. Testing Localization

```dart
void main() {
  testWidgets('displays localized text in Turkish', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        locale: Locale('tr'),
        localizationsDelegates: AppLocalizations.localizationsDelegates,
        supportedLocales: AppLocalizations.supportedLocales,
        home: HomePage(),
      ),
    );

    expect(find.text('Hoş geldin!'), findsOneWidget);
  });

  testWidgets('handles pluralization correctly', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        locale: Locale('en'),
        localizationsDelegates: AppLocalizations.localizationsDelegates,
        supportedLocales: AppLocalizations.supportedLocales,
        home: Builder(
          builder: (context) {
            return Column(
              children: [
                Text(AppLocalizations.of(context).itemCount(0)),
                Text(AppLocalizations.of(context).itemCount(1)),
                Text(AppLocalizations.of(context).itemCount(5)),
              ],
            );
          },
        ),
      ),
    );

    expect(find.text('No items'), findsOneWidget);
    expect(find.text('1 item'), findsOneWidget);
    expect(find.text('5 items'), findsOneWidget);
  });

  testWidgets('RTL layout is correct for Arabic', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        locale: Locale('ar'),
        localizationsDelegates: [
          GlobalMaterialLocalizations.delegate,
          GlobalWidgetsLocalizations.delegate,
        ],
        supportedLocales: [Locale('ar')],
        home: HomePage(),
      ),
    );

    final direction = Directionality.of(tester.element(find.byType(HomePage)));
    expect(direction, TextDirection.rtl);
  });
}
```

## 6. slang Package Alternative

```dart
// Alternative: slang package for type-safe translations
// slang.yaml
base_locale: en
input_directory: lib/i18n
output_directory: lib/gen

// lib/i18n/strings_en.i18n.json
{
  "greeting": "Hello $name",
  "items": {
    "zero": "No items",
    "one": "One item",
    "other": "$n items"
  }
}

// Usage
Text(t.greeting(name: 'John'))
Text(t.items(n: 5))
```

## Troubleshooting Guide

**Issue: Localization not loading**
```
1. Run: flutter gen-l10n
2. Verify l10n.yaml in project root
3. Check ARB file syntax (valid JSON)
4. Ensure flutter: generate: true in pubspec.yaml
5. Import: flutter_gen/gen_l10n/app_localizations.dart
```

**Issue: Locale not recognized**
```
1. Verify locale is in supportedLocales
2. Check locale code format (en vs en_US)
3. Ensure localizationsDelegates includes your delegate
4. Check @@locale in ARB file matches
```

**Issue: Placeholders not working**
```
1. Verify placeholder name matches exactly
2. Check placeholder type in @message
3. Ensure placeholder syntax: {name}
4. Run flutter gen-l10n to regenerate
```

**Issue: RTL not applying**
```
1. Add GlobalWidgetsLocalizations.delegate
2. Use Directional variants (EdgeInsetsDirectional)
3. Check Directionality widget wrapping
4. Verify locale is RTL language
```

## Localization Best Practices

```
1. Never hardcode strings in widgets
2. Use descriptive keys (settingsPageTitle vs title)
3. Include context in @descriptions
4. Test all supported locales
5. Handle long text gracefully (overflow)
6. Use ICU message format for complex cases
7. Keep translations organized by feature
8. Review with native speakers
```

---

**Build globally accessible Flutter apps with proper localization.**
