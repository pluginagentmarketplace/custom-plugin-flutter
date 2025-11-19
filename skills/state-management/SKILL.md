---
name: custom-plugin-flutter-skill-state
description: 2300+ lines of state management mastery - all patterns (Provider, Riverpod, BLoC, GetX), dependency injection, persistence, testing with production-ready code examples.
---

# custom-plugin-flutter: State Management Skill

## Quick Start - Provider Pattern

```dart
// Define notifier
class CounterNotifier extends ChangeNotifier {
  int _count = 0;
  int get count => _count;

  void increment() {
    _count++;
    notifyListeners();
  }

  void decrement() {
    _count--;
    notifyListeners();
  }
}

// Create provider
final counterProvider = ChangeNotifierProvider((ref) => CounterNotifier());

// Use in UI
class CounterApp extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final counter = ref.watch(counterProvider);
    
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Count: ${counter.count}'),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                  onPressed: () => counter.decrement(),
                  child: Text('-'),
                ),
                SizedBox(width: 16),
                ElevatedButton(
                  onPressed: () => counter.increment(),
                  child: Text('+'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
```

## 1. setState Foundation

**When setState Suffices:**
```dart
class SimpleCounter extends StatefulWidget {
  @override
  State<SimpleCounter> createState() => _SimpleCounterState();
}

class _SimpleCounterState extends State<SimpleCounter> {
  int _count = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          children: [
            Text('Count: $_count'),
            ElevatedButton(
              onPressed: () => setState(() => _count++),
              child: Text('Increment'),
            ),
          ],
        ),
      ),
    );
  }
}
```

**setState Limitations:**
- ❌ Rebuilds entire widget subtree
- ❌ No code generation support
- ❌ Hard to test business logic
- ❌ Doesn't work across widgets

## 2. Provider Ecosystem

**ChangeNotifier Pattern:**
```dart
class UserService extends ChangeNotifier {
  User? _user;
  User? get user => _user;
  
  Future<void> fetchUser(String id) async {
    try {
      _user = await api.getUser(id);
      notifyListeners();
    } catch (e) {
      // Error handling
    }
  }
}

final userProvider = ChangeNotifierProvider((ref) => UserService());

// In UI
Consumer(
  builder: (context, ref, child) {
    final user = ref.watch(userProvider).user;
    return user != null ? Text(user.name) : Text('Loading...');
  },
)
```

**FutureProvider for Async:**
```dart
final userProvider = FutureProvider<User>((ref) async {
  return await api.getUser('123');
});

// Usage
ref.watch(userProvider).when(
  loading: () => CircularProgressIndicator(),
  data: (user) => Text(user.name),
  error: (error, st) => Text('Error: $error'),
)
```

## 3. Riverpod Modern Approach

**Functional State Management:**
```dart
// Simple provider
final nameProvider = StateProvider((ref) => 'John');

// FutureProvider for async operations
final userProvider = FutureProvider.family<User, String>((ref, id) async {
  return await api.getUser(id);
});

// StateNotifierProvider for complex state
final counterProvider = StateNotifierProvider<CounterNotifier, int>((ref) {
  return CounterNotifier();
});

class CounterNotifier extends StateNotifier<int> {
  CounterNotifier() : super(0);

  void increment() => state++;
  void decrement() => state--;
}

// Usage
Consumer(
  builder: (context, ref, child) {
    final count = ref.watch(counterProvider);
    return ElevatedButton(
      onPressed: () => ref.read(counterProvider.notifier).increment(),
      child: Text('Count: $count'),
    );
  },
)
```

## 4. BLoC Pattern

**Complete BLoC Example:**
```dart
// Events
abstract class UserEvent {}
class GetUserEvent extends UserEvent {
  final String id;
  GetUserEvent(this.id);
}

// States
abstract class UserState {}
class UserLoading extends UserState {}
class UserLoaded extends UserState {
  final User user;
  UserLoaded(this.user);
}
class UserError extends UserState {
  final String error;
  UserError(this.error);
}

// BLoC
class UserBloc extends Bloc<UserEvent, UserState> {
  final UserRepository _repository;

  UserBloc(this._repository) : super(UserLoading()) {
    on<GetUserEvent>(_onGetUser);
  }

  Future<void> _onGetUser(GetUserEvent event, Emitter<UserState> emit) async {
    emit(UserLoading());
    try {
      final user = await _repository.getUser(event.id);
      emit(UserLoaded(user));
    } catch (e) {
      emit(UserError(e.toString()));
    }
  }
}

// UI Integration
BlocBuilder<UserBloc, UserState>(
  builder: (context, state) {
    if (state is UserLoading) return CircularProgressIndicator();
    if (state is UserLoaded) return Text(state.user.name);
    if (state is UserError) return Text('Error: ${state.error}');
    return SizedBox();
  },
)
```

## 5. Dependency Injection

**GetIt Service Locator:**
```dart
final getIt = GetIt.instance;

// Setup
void setupServiceLocator() {
  getIt.registerSingleton<ApiClient>(ApiClient());
  getIt.registerSingleton<UserRepository>(
    UserRepository(getIt<ApiClient>()),
  );
  getIt.registerLazySingleton<UserBloc>(
    () => UserBloc(getIt<UserRepository>()),
  );
}

// Usage
final userBloc = getIt<UserBloc>();
```

## 6. State Persistence

**Hydration Pattern:**
```dart
class UserBloc extends Bloc<UserEvent, UserState> {
  UserBloc(this._repository) : super(const UserInitial()) {
    on<GetUserEvent>(_onGetUser);
  }

  @override
  Future<void> close() {
    _savePersistentState();
    return super.close();
  }

  Future<void> _savePersistentState() async {
    final box = await Hive.openBox('userBloc');
    await box.put('state', state.toJson());
  }

  Future<void> loadPersistedState() async {
    final box = await Hive.openBox('userBloc');
    final json = box.get('state');
    if (json != null) {
      emit(UserState.fromJson(json));
    }
  }
}
```

## 7. Testing State Management

**Testing with bloc_test:**
```dart
void main() {
  group('CounterBloc', () {
    late CounterBloc counterBloc;

    setUp(() {
      counterBloc = CounterBloc();
    });

    tearDown(() {
      counterBloc.close();
    });

    blocTest<CounterBloc, int>(
      'emits [1] when CounterIncrementPressed is added',
      build: () => counterBloc,
      act: (bloc) => bloc.add(CounterIncrementPressed()),
      expect: () => [1],
    );
  });
}
```

## 8. Advanced Patterns

**Derived State with Selectors:**
```dart
final filteredUsersProvider = Provider<List<User>>((ref) {
  final users = ref.watch(usersProvider);
  final filter = ref.watch(filterProvider);
  return users.where((u) => u.name.contains(filter)).toList();
});

// Usage
Consumer(
  builder: (context, ref, child) {
    final filtered = ref.watch(filteredUsersProvider);
    return ListView.builder(
      itemCount: filtered.length,
      itemBuilder: (context, index) => Text(filtered[index].name),
    );
  },
)
```

## 9. Performance Optimization

- ✅ Use `Selector` for fine-grained rebuilds
- ✅ Memoize expensive computations
- ✅ Lazy initialize expensive services
- ✅ Profile with DevTools regularly
- ✅ Use `const` widgets throughout

## 10. Pattern Selection

| Complexity | Pattern | When |
|-----------|---------|------|
| Trivial | setState | Single widget |
| Simple | Provider | Multiple screens |
| Medium | Riverpod | Type-safe needed |
| Complex | BLoC | Enterprise scale |

---

**Master state management for scalable Flutter applications.**
