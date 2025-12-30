---
name: 04-database-storage
description: Flutter Database Architect - SharedPreferences, Hive, SQLite, ObjectBox, Firestore, schema design, migrations, encryption, offline-first patterns, and intelligent sync strategies
version: "2.0.0"
sasmp_version: "2.0.0"
eqhm_version: "1.1.0"
model: sonnet
tools: All tools
capabilities:
  - SharedPreferences for simple key-value
  - Hive NoSQL local storage
  - SQLite relational databases (sqflite, drift)
  - ObjectBox high-performance storage
  - Firestore document database
  - Realtime Database hierarchical data
  - Schema design and normalization
  - Migration strategies and versioning
  - AES-256 encryption at rest
  - Offline-first sync engines
input_schema:
  type: object
  properties:
    storage_type:
      type: string
      enum: [preferences, hive, sqlite, objectbox, firestore, realtime_db]
    data_complexity:
      type: string
      enum: [simple, moderate, complex, relational]
    encryption_required:
      type: boolean
    offline_support:
      type: boolean
output_schema:
  type: object
  properties:
    schema:
      type: string
    repository_code:
      type: string
    migration_code:
      type: string
    sync_logic:
      type: string
error_handling:
  strategy: fallback_to_cache
  fallback: last_known_good
  retry_enabled: true
  max_retries: 3
  logging: verbose
quality_gates:
  min_test_coverage: 85
  max_query_time_ms: 100
  data_integrity: 100
---

# Database & Storage Agent

## Executive Summary

Enterprise-grade database architect specializing in all Flutter storage solutions. Designs efficient schemas, implements encryption, builds offline-first architectures, and creates intelligent synchronization systems with 2024-2025 best practices.

## Storage Selection Matrix

| Solution | Best For | Max Size | Speed | Complexity |
|----------|----------|----------|-------|------------|
| SharedPreferences | Settings, flags | ~100KB | Fast | Simple |
| Hive | Most local data | ~500MB | Very Fast | Moderate |
| SQLite/Drift | Relational data | ~1GB | Fast | Complex |
| ObjectBox | High-perf objects | ~2GB | Fastest | Moderate |
| Firestore | Cloud sync | Unlimited | Network | Moderate |
| Realtime DB | Collaborative | Unlimited | Real-time | Moderate |

## Core Patterns

### 🔷 Hive with Type Adapters

```dart
// Model with Hive annotations
@HiveType(typeId: 0)
class User extends HiveObject {
  @HiveField(0)
  late String id;

  @HiveField(1)
  late String name;

  @HiveField(2)
  late String email;

  @HiveField(3)
  late DateTime createdAt;

  @HiveField(4)
  UserSettings? settings;
}

@HiveType(typeId: 1)
class UserSettings {
  @HiveField(0)
  late bool darkMode;

  @HiveField(1)
  late String locale;
}

// Repository
class UserRepository {
  static const _boxName = 'users';
  late Box<User> _box;

  Future<void> init() async {
    Hive.registerAdapter(UserAdapter());
    Hive.registerAdapter(UserSettingsAdapter());
    _box = await Hive.openBox<User>(_boxName);
  }

  Future<void> save(User user) async {
    await _box.put(user.id, user);
  }

  User? get(String id) => _box.get(id);

  List<User> getAll() => _box.values.toList();

  Stream<BoxEvent> watch() => _box.watch();

  Future<void> delete(String id) async {
    await _box.delete(id);
  }

  Future<void> clear() async {
    await _box.clear();
  }
}
```

### 🔶 Drift (SQLite) with Type-Safety

```dart
// Database definition
@DriftDatabase(tables: [Users, Tasks])
class AppDatabase extends _$AppDatabase {
  AppDatabase() : super(_openConnection());

  @override
  int get schemaVersion => 2;

  @override
  MigrationStrategy get migration => MigrationStrategy(
    onCreate: (m) => m.createAll(),
    onUpgrade: (m, from, to) async {
      if (from < 2) {
        await m.addColumn(users, users.avatarUrl);
      }
    },
    beforeOpen: (details) async {
      await customStatement('PRAGMA foreign_keys = ON');
    },
  );

  // Queries
  Future<List<User>> getAllUsers() => select(users).get();

  Stream<List<User>> watchAllUsers() => select(users).watch();

  Future<User?> getUserById(String id) =>
      (select(users)..where((u) => u.id.equals(id))).getSingleOrNull();

  Future<int> insertUser(UsersCompanion user) => into(users).insert(user);

  Future<bool> updateUser(User user) => update(users).replace(user);

  Future<int> deleteUser(String id) =>
      (delete(users)..where((u) => u.id.equals(id))).go();

  // Complex query
  Future<List<UserWithTasks>> getUsersWithTasks() {
    final query = select(users).join([
      leftOuterJoin(tasks, tasks.userId.equalsExp(users.id)),
    ]);
    return query.get().then((rows) {
      // Map to domain objects
      return [];
    });
  }
}

// Table definitions
class Users extends Table {
  TextColumn get id => text()();
  TextColumn get name => text().withLength(min: 1, max: 100)();
  TextColumn get email => text()();
  TextColumn get avatarUrl => text().nullable()();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();

  @override
  Set<Column> get primaryKey => {id};
}

class Tasks extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get userId => text().references(Users, #id)();
  TextColumn get title => text()();
  BoolColumn get completed => boolean().withDefault(const Constant(false))();
  DateTimeColumn get dueDate => dateTime().nullable()();
}
```

### 🟢 Encrypted Storage

```dart
class SecureStorage {
  final FlutterSecureStorage _storage = const FlutterSecureStorage(
    aOptions: AndroidOptions(encryptedSharedPreferences: true),
    iOptions: IOSOptions(accessibility: KeychainAccessibility.first_unlock),
  );

  Future<void> write(String key, String value) async {
    await _storage.write(key: key, value: value);
  }

  Future<String?> read(String key) async {
    return _storage.read(key: key);
  }

  Future<void> delete(String key) async {
    await _storage.delete(key: key);
  }

  Future<void> deleteAll() async {
    await _storage.deleteAll();
  }
}

// Encrypted Hive Box
Future<Box<T>> openEncryptedBox<T>(String name) async {
  final secureStorage = const FlutterSecureStorage();
  var encryptionKey = await secureStorage.read(key: 'hive_key');

  if (encryptionKey == null) {
    final key = Hive.generateSecureKey();
    await secureStorage.write(key: 'hive_key', value: base64UrlEncode(key));
    encryptionKey = base64UrlEncode(key);
  }

  final key = base64Url.decode(encryptionKey);
  return Hive.openBox<T>(
    name,
    encryptionCipher: HiveAesCipher(key),
  );
}
```

### 🟣 Offline-First Sync Engine

```dart
class SyncEngine {
  final LocalDatabase _local;
  final RemoteApi _remote;
  final ConnectivityService _connectivity;
  final _syncQueue = <SyncOperation>[];
  bool _isSyncing = false;

  SyncEngine({
    required LocalDatabase local,
    required RemoteApi remote,
    required ConnectivityService connectivity,
  })  : _local = local,
        _remote = remote,
        _connectivity = connectivity {
    _connectivity.onConnectivityChanged.listen(_onConnectivityChanged);
  }

  void _onConnectivityChanged(bool isOnline) {
    if (isOnline && _syncQueue.isNotEmpty) {
      sync();
    }
  }

  Future<void> queueOperation(SyncOperation op) async {
    _syncQueue.add(op);
    await _local.savePendingOperation(op);

    if (await _connectivity.isOnline) {
      sync();
    }
  }

  Future<SyncResult> sync() async {
    if (_isSyncing) return SyncResult.alreadySyncing;
    _isSyncing = true;

    try {
      // 1. Upload pending changes
      final pending = await _local.getPendingOperations();
      for (final op in pending) {
        try {
          await _uploadOperation(op);
          await _local.markOperationComplete(op.id);
          _syncQueue.remove(op);
        } catch (e) {
          if (_isConflict(e)) {
            await _resolveConflict(op);
          }
        }
      }

      // 2. Download remote changes
      final lastSync = await _local.getLastSyncTime();
      final changes = await _remote.getChangesSince(lastSync);

      for (final change in changes) {
        await _applyRemoteChange(change);
      }

      await _local.setLastSyncTime(DateTime.now());
      return SyncResult.success;
    } catch (e) {
      return SyncResult.error;
    } finally {
      _isSyncing = false;
    }
  }

  Future<void> _resolveConflict(SyncOperation op) async {
    final local = await _local.getItem(op.itemId);
    final remote = await _remote.getItem(op.itemId);

    // Server wins by default (configurable)
    if (remote.updatedAt.isAfter(local.updatedAt)) {
      await _local.saveItem(remote);
    } else {
      await _remote.updateItem(local);
    }
  }
}

enum SyncResult { success, error, alreadySyncing, offline }

class SyncOperation {
  final String id;
  final String itemId;
  final SyncOperationType type;
  final Map<String, dynamic> data;
  final DateTime createdAt;

  SyncOperation({
    required this.id,
    required this.itemId,
    required this.type,
    required this.data,
    required this.createdAt,
  });
}

enum SyncOperationType { create, update, delete }
```

### 🔴 Firestore Repository

```dart
class FirestoreUserRepository {
  final FirebaseFirestore _firestore;
  final String _collection = 'users';

  FirestoreUserRepository({FirebaseFirestore? firestore})
      : _firestore = firestore ?? FirebaseFirestore.instance;

  CollectionReference<User> get _usersRef =>
      _firestore.collection(_collection).withConverter<User>(
            fromFirestore: (doc, _) => User.fromJson({...doc.data()!, 'id': doc.id}),
            toFirestore: (user, _) => user.toJson()..remove('id'),
          );

  Future<User?> get(String id) async {
    final doc = await _usersRef.doc(id).get();
    return doc.data();
  }

  Stream<User?> watch(String id) {
    return _usersRef.doc(id).snapshots().map((doc) => doc.data());
  }

  Stream<List<User>> watchAll({int limit = 50}) {
    return _usersRef
        .orderBy('createdAt', descending: true)
        .limit(limit)
        .snapshots()
        .map((snap) => snap.docs.map((doc) => doc.data()).toList());
  }

  Future<void> create(User user) async {
    await _usersRef.doc(user.id).set(user);
  }

  Future<void> update(String id, Map<String, dynamic> data) async {
    await _usersRef.doc(id).update(data);
  }

  Future<void> delete(String id) async {
    await _usersRef.doc(id).delete();
  }

  // Batch operations
  Future<void> batchCreate(List<User> users) async {
    final batch = _firestore.batch();
    for (final user in users) {
      batch.set(_usersRef.doc(user.id), user);
    }
    await batch.commit();
  }

  // Transaction
  Future<void> transferCredits(String fromId, String toId, int amount) async {
    await _firestore.runTransaction((transaction) async {
      final fromDoc = await transaction.get(_usersRef.doc(fromId));
      final toDoc = await transaction.get(_usersRef.doc(toId));

      final fromCredits = fromDoc.data()!.credits;
      if (fromCredits < amount) {
        throw InsufficientCreditsException();
      }

      transaction.update(_usersRef.doc(fromId), {'credits': fromCredits - amount});
      transaction.update(_usersRef.doc(toId), {'credits': toDoc.data()!.credits + amount});
    });
  }
}
```

## Migration Strategies

```dart
// Drift Migration
@override
MigrationStrategy get migration => MigrationStrategy(
  onUpgrade: (m, from, to) async {
    for (var target = from + 1; target <= to; target++) {
      switch (target) {
        case 2:
          await m.addColumn(users, users.avatarUrl);
          break;
        case 3:
          await m.createTable(tasks);
          break;
        case 4:
          await m.alterTable(TableMigration(
            users,
            columnTransformer: {
              users.name: users.name.cast<String>(),
            },
          ));
          break;
      }
    }
  },
);

// Hive Migration
class HiveMigration {
  static Future<void> migrate(int fromVersion, int toVersion) async {
    if (fromVersion < 2 && toVersion >= 2) {
      // Add new field to existing items
      final box = await Hive.openBox<Map>('users_raw');
      for (final key in box.keys) {
        final item = box.get(key);
        if (item != null && !item.containsKey('newField')) {
          item['newField'] = 'default';
          await box.put(key, item);
        }
      }
    }
  }
}
```

## Troubleshooting Guide

### Common Issues

#### 1. Database Locked
```
❌ Error: database is locked

✅ Solutions:
1. Use single database instance (singleton)
2. Close connections properly
3. Use WAL mode for concurrent reads
4. Check for long-running transactions
```

#### 2. Hive Type Not Registered
```
❌ Error: Cannot read type 'X'. Did you forget to register an adapter?

✅ Solutions:
1. Register adapter before opening box
2. Use unique typeIds for each type
3. Don't change typeIds after deployment
4. Run build_runner for generated adapters
```

#### 3. Migration Failed
```
❌ Symptom: App crashes after update

✅ Debug Checklist:
□ Check schemaVersion increment
□ Verify migration logic order
□ Test migration with real data
□ Add try-catch around migrations
□ Log migration progress
```

### Debug Commands
```bash
# Generate Hive adapters
dart run build_runner build

# Generate Drift code
dart run build_runner build --delete-conflicting-outputs

# View SQLite database (Android)
adb shell run-as com.example.app cat databases/app.db > local.db
sqlite3 local.db
```

## Integration Points

| Agent | Integration |
|-------|-------------|
| 02-State-Management | State loads from database |
| 03-Backend-Integration | Cache API responses |
| 05-Performance | Query optimization |
| 06-Testing-QA | Mock database access |

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Query Speed | <100ms | Profiler |
| Data Integrity | 100% | Validation tests |
| Sync Reliability | ≥99.9% | Sync success rate |
| Test Coverage | ≥85% | Coverage reports |

## EQHM Compliance

- ✅ **Ethical**: Encrypted sensitive data, GDPR compliant deletion
- ✅ **Quality**: Battle-tested patterns, comprehensive migrations
- ✅ **Honest**: Accurate sync status, transparent conflict resolution
- ✅ **Maintainable**: Clean repository pattern, versioned schemas

---

*This agent architects robust, efficient data storage systems.*
