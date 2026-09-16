import 'package:dartz/dartz.dart';
import '../error/failures.dart';

abstract class UseCase<R, Params> {
  Future<Either<Failure, R>> call(Params params);
}

class NoParams {}
