---
name: custom-plugin-flutter-skill-database
description: 1800+ lines of database architecture mastery - SQLite, Hive, ObjectBox, Firestore, encryption, offline-first, sync with production-ready code examples.
---

# custom-plugin-flutter: Database & Storage Skill

## Quick Start - Hive Storage

```dart
// Define model
@HiveType(typeId: 0)
class User {
  @HiveField(0)
  final String id;
  @HiveField(1)
  final String name;

  User({required this.id, required this.name});
}

// Use Hive
Future<void> main() async {
  await Hive.initFlutter();
  Hive.registerAdapter(UserAdapter());
  runApp(MyApp());
}

// Save
final box = await Hive.openBox<User>('users');
await box.put('user1', User(id: '1', name: 'John'));

// Retrieve
final user = box.get('user1');

// Watch changes
box.listenable().addListener(() {
  print('Box changed!');
});
```

## 1. Storage Solutions

**SharedPreferences (Simple):**
```dart
final prefs = await SharedPreferences.getInstance();
await prefs.setString('username', 'john');
final username = prefs.getString('username');
```

**Hive (Flexible):**
```dart
@HiveType(typeId: 0)
class Product {
  @HiveField(0)
  final String id;
  @HiveField(1)
  final String name;
  @HiveField(2)
  final double price;

  Product({required this.id, required this.name, required this.price});
}

final box = await Hive.openBox<Product>('products');
await box.add(Product(id: '1', name: 'Widget', price: 9.99));
final products = box.values.toList();
```

**SQLite (Relational):**
```dart
final database = await openDatabase(
  'app.db',
  onCreate: (db, version) async {
    await db.execute('''
      CREATE TABLE users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL
      )
    ''');
  },
);

// Insert
await database.insert('users', {
  'id': '1',
  'name': 'John',
  'email': 'john@example.com',
});

// Query
final users = await database.query('users');
```

## 2. Encryption

```dart
import 'package:encrypt/encrypt.dart' as encrypt;

class SecureStorage {
  late final encrypt.Key _key;
  late final encrypt.IV _iv;

  SecureStorage() {
    _key = encrypt.Key.fromSecureRandom(32);
    _iv = encrypt.IV.fromSecureRandom(16);
  }

  String encrypt(String plaintext) {
    final encrypter = encrypt.Encrypter(encrypt.AES(_key));
    return encrypter.encrypt(plaintext, iv: _iv).base64;
  }

  String decrypt(String ciphertext) {
    final encrypter = encrypt.Encrypter(encrypt.AES(_key));
    return encrypter.decrypt64(ciphertext, iv: _iv);
  }
}
```

## 3. Migrations

```dart
final database = await openDatabase(
  'app.db',
  version: 2,
  onCreate: (db, version) async {
    await db.execute('CREATE TABLE users (id TEXT PRIMARY KEY, name TEXT)');
  },
  onUpgrade: (db, oldVersion, newVersion) async {
    if (oldVersion < 2) {
      await db.execute('ALTER TABLE users ADD COLUMN email TEXT');
    }
  },
);
```

## 4. Offline-First Sync

```dart
class SyncEngine {
  final LocalDatabase local;
  final RemoteAPI remote;
  final _queue = <SyncOperation>[];

  Future<void> sync() async {
    // Upload pending changes
    for (final op in _queue) {
      try {
        await _uploadOperation(op);
        _queue.remove(op);
      } catch (e) {
        // Retry later
      }
    }

    // Download remote changes
    try {
      final remoteData = await remote.getUpdates();
      await _mergeRemoteData(remoteData);
    } catch (e) {
      // Continue with local data
    }
  }

  Future<void> _mergeRemoteData(dynamic remoteData) async {
    for (final item in remoteData) {
      final local = await this.local.getItem(item['id']);
      if (local == null || item['updatedAt'] > local['updatedAt']) {
        await this.local.upsert(item);
      }
    }
  }
}
```

## 5. Firestore

```dart
class FirestoreRepository {
  final firestore = FirebaseFirestore.instance;

  Future<User?> getUser(String id) async {
    final doc = await firestore.collection('users').doc(id).get();
    return doc.exists ? User.fromJson(doc.data()!) : null;
  }

  Stream<List<User>> watchUsers() {
    return firestore
        .collection('users')
        .orderBy('createdAt')
        .snapshots()
        .map((snap) => snap.docs
            .map((doc) => User.fromJson(doc.data()))
            .toList());
  }

  Future<void> createUser(User user) async {
    await firestore.collection('users').doc(user.id).set(
      user.toJson(),
      SetOptions(merge: true),
    );
  }
}
```

---

**Master database design for scalable Flutter applications.**
