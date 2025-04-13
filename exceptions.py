from fastapi import HTTPException, status


class SException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(SException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует!"


class IncorrectEmailOrPasswordException(SException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неправильная почта или пароль!"


class TokenExpiredException(SException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия вашего токена истёк!"


class TokenMissingException(SException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токена не существует!"


class IncorrectTokenFormatException(SException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неправильный формат токена!"


class IncorrectInformationUserException(SException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBooked(SException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров!"


class UnknownHotel(SException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не существует такого отеля!"


class UnknownBooking(SException):
    status_code = status.HTTP_409_CONFLICT
    detail = "У вас не существует такой брони!"


class NotBooking(SException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Нет бронирований!"


class IncorrectDate(SException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Дата заезда больше даты выезда!"


class IncorrectDateDays(SException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Период больше 30 дней!"


class CannotAddDataToDatabase(SException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ('Не удалось добавить запись в базу данных. '
              'Проверьте корректность данных.')


class CannotProcessCSV(SException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось обработать CSV файл!"
