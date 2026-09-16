import '../models/user_model.dart';

abstract class UserRemoteDataSource {
  Future<List<UserModel>> getUsers();
}

class UserRemoteDataSourceImpl implements UserRemoteDataSource {
  @override
  Future<List<UserModel>> getUsers() async {
    // Simulate network delay
    await Future.delayed(const Duration(seconds: 2));
    
    // Simulate a successful response with mock data
    return [
      const UserModel(id: 1, name: 'Alice Smith', email: 'alice@example.com'),
      const UserModel(id: 2, name: 'Bob Johnson', email: 'bob@example.com'),
      const UserModel(id: 3, name: 'Charlie Brown', email: 'charlie@example.com'),
    ];
  }
}
