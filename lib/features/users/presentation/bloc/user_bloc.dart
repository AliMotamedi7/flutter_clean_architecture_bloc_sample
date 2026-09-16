import 'package:flutter_bloc/flutter_bloc.dart';
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
