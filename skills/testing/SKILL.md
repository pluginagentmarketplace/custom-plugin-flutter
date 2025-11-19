---
name: custom-plugin-flutter-skill-testing
description: 1600+ lines of testing mastery - unit tests, widget tests, integration tests, E2E, coverage, mocking with production-ready code examples.
---

# custom-plugin-flutter: Testing & QA Skill

## Quick Start - Complete Test Suite

```dart
// Unit test
void main() {
  group('Calculator', () {
    late Calculator calc;

    setUp(() {
      calc = Calculator();
    });

    test('add returns sum', () {
      expect(calc.add(2, 3), equals(5));
    });
  });
}

// Widget test
void main() {
  testWidgets('Counter increments', (tester) async {
    await tester.pumpWidget(const MyApp());
    expect(find.text('0'), findsOneWidget);

    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();

    expect(find.text('1'), findsOneWidget);
  });
}

// Integration test
void main() {
  group('User Flow', () {
    testWidgets('Complete user journey', (tester) async {
      await tester.pumpWidget(const MyApp());
      
      await tester.tap(find.text('Login'));
      await tester.pumpAndSettle();

      expect(find.text('Welcome'), findsOneWidget);
    });
  });
}
```

## 1. Unit Testing

```dart
class UserService {
  Future<User> getUser(String id) async {
    // Implementation
  }
}

void main() {
  group('UserService', () {
    late UserService service;
    late MockUserRepository mockRepository;

    setUp(() {
      mockRepository = MockUserRepository();
      service = UserService(mockRepository);
    });

    test('getUser returns user', () async {
      final user = User(id: '1', name: 'John');
      when(mockRepository.getUser('1')).thenAnswer((_) async => user);

      final result = await service.getUser('1');

      expect(result, user);
      verify(mockRepository.getUser('1')).called(1);
    });

    test('getUser throws on error', () async {
      when(mockRepository.getUser('1'))
          .thenThrow(Exception('Not found'));

      expect(
        () => service.getUser('1'),
        throwsException,
      );
    });
  });
}
```

## 2. Widget Testing

```dart
void main() {
  testWidgets('Render user card', (tester) async {
    const user = User(id: '1', name: 'John Doe', email: 'john@example.com');

    await tester.pumpWidget(
      MaterialApp(home: Scaffold(body: UserCard(user: user))),
    );

    expect(find.text('John Doe'), findsOneWidget);
    expect(find.text('john@example.com'), findsOneWidget);
  });

  testWidgets('Tap user card navigates', (tester) async {
    const user = User(id: '1', name: 'John Doe', email: 'john@example.com');

    await tester.pumpWidget(MaterialApp(home: Scaffold(body: UserCard(user: user))));

    await tester.tap(find.byType(UserCard));
    await tester.pumpAndSettle();

    expect(find.byType(UserDetailPage), findsOneWidget);
  });
}
```

## 3. Mocking

```dart
class MockUserRepository extends Mock implements UserRepository {}

final mockRepository = MockUserRepository();

// Setup mock behavior
when(mockRepository.getUser('1')).thenAnswer((_) async => User(...));

// Verify calls
verify(mockRepository.getUser('1')).called(1);

// Capture arguments
final captured = verify(mockRepository.updateUser(captureAny)).captured;
```

## 4. Integration Testing

```dart
void main() {
  group('User Creation Flow', () {
    testWidgets('Create user and verify', (tester) async {
      await tester.pumpWidget(const MyApp());

      // Navigate to create user
      await tester.tap(find.text('Add User'));
      await tester.pumpAndSettle();

      // Fill form
      await tester.enterText(find.byKey(Key('nameField')), 'John');
      await tester.enterText(find.byKey(Key('emailField')), 'john@example.com');

      // Submit
      await tester.tap(find.text('Create'));
      await tester.pumpAndSettle();

      // Verify result
      expect(find.text('User created'), findsOneWidget);
    });
  });
}
```

---

**Ensure bulletproof quality with comprehensive testing.**
