import os

files = {
    "lib/core/error/failures.dart": """import 'package:equatable/equatable.dart';

abstract class Failure extends Equatable {
  final String message;
  const Failure(this.message);

  @override
  List<Object> get props => [message];
}

class ServerFailure extends Failure {
  const ServerFailure(super.message);
}

class CacheFailure extends Failure {
  const CacheFailure(super.message);
}
""",
    "lib/core/usecases/usecase.dart": """import 'package:dartz/dartz.dart';
import '../error/failures.dart';

abstract class UseCase<Type, Params> {
  Future<Either<Failure, Type>> call(Params params);
}

class NoParams {}
""",
    "lib/core/di/injection_container.dart": """import 'package:get_it/get_it.dart';
import '../../features/users/domain/repositories/user_repository.dart';
import '../../features/users/data/repositories/user_repository_impl.dart';
import '../../features/users/data/datasources/user_remote_data_source.dart';
import '../../features/users/domain/usecases/get_users.dart';
import '../../features/users/presentation/bloc/user_bloc.dart';

final sl = GetIt.instance;

Future<void> init() async {
  // Features - Users
  // Bloc
  sl.registerFactory(() => UserBloc(getUsers: sl()));

  // Use cases
  sl.registerLazySingleton(() => GetUsers(sl()));

  // Repository
  sl.registerLazySingleton<UserRepository>(
    () => UserRepositoryImpl(remoteDataSource: sl()),
  );

  // Data sources
  sl.registerLazySingleton<UserRemoteDataSource>(
    () => UserRemoteDataSourceImpl(),
  );
}
""",
    "lib/features/users/domain/entities/user.dart": """import 'package:equatable/equatable.dart';

class User extends Equatable {
  final int id;
  final String name;
  final String email;

  const User({
    required this.id,
    required this.name,
    required this.email,
  });

  @override
  List<Object> get props => [id, name, email];
}
""",
    "lib/features/users/domain/repositories/user_repository.dart": """import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/user.dart';

abstract class UserRepository {
  Future<Either<Failure, List<User>>> getUsers();
}
""",
    "lib/features/users/domain/usecases/get_users.dart": """import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../../../../core/usecases/usecase.dart';
import '../entities/user.dart';
import '../repositories/user_repository.dart';

class GetUsers implements UseCase<List<User>, NoParams> {
  final UserRepository repository;

  GetUsers(this.repository);

  @override
  Future<Either<Failure, List<User>>> call(NoParams params) {
    return repository.getUsers();
  }
}
""",
    "lib/features/users/data/models/user_model.dart": """import '../../domain/entities/user.dart';

class UserModel extends User {
  const UserModel({
    required super.id,
    required super.name,
    required super.email,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'],
      name: json['name'],
      email: json['email'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
    };
  }
}
""",
    "lib/features/users/data/datasources/user_remote_data_source.dart": """import '../models/user_model.dart';
import '../../../../core/error/failures.dart';

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
""",
    "lib/features/users/data/repositories/user_repository_impl.dart": """import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/user_repository.dart';
import '../datasources/user_remote_data_source.dart';

class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource remoteDataSource;

  UserRepositoryImpl({required this.remoteDataSource});

  @override
  Future<Either<Failure, List<User>>> getUsers() async {
    try {
      final remoteUsers = await remoteDataSource.getUsers();
      return Right(remoteUsers);
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }
}
""",
    "lib/features/users/presentation/bloc/user_event.dart": """import 'package:equatable/equatable.dart';

abstract class UserEvent extends Equatable {
  const UserEvent();

  @override
  List<Object> get props => [];
}

class GetUsersEvent extends UserEvent {}
""",
    "lib/features/users/presentation/bloc/user_state.dart": """import 'package:equatable/equatable.dart';
import '../../domain/entities/user.dart';

abstract class UserState extends Equatable {
  const UserState();

  @override
  List<Object> get props => [];
}

class UserInitial extends UserState {}

class UserLoading extends UserState {}

class UserLoaded extends UserState {
  final List<User> users;

  const UserLoaded({required this.users});

  @override
  List<Object> get props => [users];
}

class UserError extends UserState {
  final String message;

  const UserError({required this.message});

  @override
  List<Object> get props => [message];
}
""",
    "lib/features/users/presentation/bloc/user_bloc.dart": """import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/usecases/usecase.dart';
import '../../domain/usecases/get_users.dart';
import 'user_event.dart';
import 'user_state.dart';

class UserBloc extends Bloc<UserEvent, UserState> {
  final GetUsers getUsers;

  UserBloc({required this.getUsers}) : super(UserInitial()) {
    on<GetUsersEvent>((event, emit) async {
      emit(UserLoading());
      
      final failureOrUsers = await getUsers(NoParams());
      
      failureOrUsers.fold(
        (failure) => emit(UserError(message: failure.message)),
        (users) => emit(UserLoaded(users: users)),
      );
    });
  }
}
""",
    "lib/features/users/presentation/widgets/user_card.dart": """import 'package:flutter/material.dart';
import '../../domain/entities/user.dart';

class UserCard extends StatelessWidget {
  final User user;

  const UserCard({super.key, required this.user});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        leading: CircleAvatar(
          backgroundColor: Theme.of(context).primaryColor.withOpacity(0.1),
          child: Text(
            user.name.substring(0, 1).toUpperCase(),
            style: TextStyle(
              color: Theme.of(context).primaryColor,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        title: Text(
          user.name,
          style: const TextStyle(fontWeight: FontWeight.bold),
        ),
        subtitle: Text(
          user.email,
          style: TextStyle(color: Colors.grey[600]),
        ),
      ),
    );
  }
}
""",
    "lib/features/users/presentation/pages/architecture_info_page.dart": """import 'package:flutter/material.dart';

class ArchitectureInfoPage extends StatelessWidget {
  const ArchitectureInfoPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Architecture Flow'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Clean Architecture + Features',
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 24),
            _buildLayerCard(
              context,
              'Presentation Layer (UI)',
              'Displays data and captures user events. Contains Pages, Widgets, and BLoC/Cubit state management.',
              Colors.blue.shade100,
            ),
            const Icon(Icons.arrow_downward, size: 32, color: Colors.grey),
            _buildLayerCard(
              context,
              'Domain Layer (Business Logic)',
              'Independent of any framework. Contains Entities, Use Cases, and Repository Interfaces.',
              Colors.green.shade100,
            ),
            const Icon(Icons.arrow_downward, size: 32, color: Colors.grey),
            _buildLayerCard(
              context,
              'Data Layer (External/Internal APIs)',
              'Fetches and parses data. Contains Models, Repository Implementations, and Data Sources.',
              Colors.orange.shade100,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLayerCard(
    BuildContext context,
    String title,
    String description,
    Color color,
  ) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.black12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: const TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 18,
            ),
          ),
          const SizedBox(height: 8),
          Text(description),
        ],
      ),
    );
  }
}
""",
    "lib/features/users/presentation/pages/users_page.dart": """import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/di/injection_container.dart';
import '../bloc/user_bloc.dart';
import '../bloc/user_event.dart';
import '../bloc/user_state.dart';
import '../widgets/user_card.dart';
import 'architecture_info_page.dart';

class UsersPage extends StatelessWidget {
  const UsersPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => sl<UserBloc>()..add(GetUsersEvent()),
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Users'),
          actions: [
            IconButton(
              icon: const Icon(Icons.info_outline),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const ArchitectureInfoPage(),
                  ),
                );
              },
            ),
          ],
        ),
        body: BlocBuilder<UserBloc, UserState>(
          builder: (context, state) {
            if (state is UserLoading) {
              return const Center(
                child: CircularProgressIndicator(),
              );
            } else if (state is UserLoaded) {
              if (state.users.isEmpty) {
                return const Center(
                  child: Text('No users found.'),
                );
              }
              return RefreshIndicator(
                onRefresh: () async {
                  context.read<UserBloc>().add(GetUsersEvent());
                },
                child: ListView.builder(
                  itemCount: state.users.length,
                  itemBuilder: (context, index) {
                    return UserCard(user: state.users[index]);
                  },
                ),
              );
            } else if (state is UserError) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.error_outline, size: 48, color: Colors.red),
                    const SizedBox(height: 16),
                    Text(
                      state.message,
                      style: const TextStyle(fontSize: 16),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: () {
                        context.read<UserBloc>().add(GetUsersEvent());
                      },
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              );
            }
            return const SizedBox.shrink();
          },
        ),
      ),
    );
  }
}
""",
    "lib/main.dart": """import 'package:flutter/material.dart';
import 'core/di/injection_container.dart' as di;
import 'features/users/presentation/pages/users_page.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await di.init();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Clean Architecture Sample',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
        fontFamily: 'Inter', // Assuming standard modern font
        appBarTheme: const AppBarTheme(
          centerTitle: true,
          elevation: 0,
        ),
      ),
      home: const UsersPage(),
    );
  }
}
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

print("Created all files successfully.")
