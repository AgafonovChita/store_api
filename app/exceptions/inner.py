from enum import IntEnum, unique
from sanic.exceptions import SanicException


@unique
class InnerError(IntEnum):
    LOGIN_ALREADY_REGISTERED = 11
    USER_IS_NOT_REGISTERED = 12
    ID_IS_NOT_REGISTERED = 13
    INSUFFICIENT_FOUNDS = 14
    WEBHOOK_SIGNATURE_IS_INVALID = 15
    PRODUCT_NOT_FOUND = 16

    def __init__(self, error_code):
        self.error_code = error_code

    @property
    def description(self):
        print(self.error_code)
        return {self.USER_IS_NOT_REGISTERED: "Пользователь с таким логин/пароль не зарегистрирован",
                self.LOGIN_ALREADY_REGISTERED: "Пользователь с таким логином уже зарегистрирован",
                self.ID_IS_NOT_REGISTERED: "Пользователь с таким ID не зарегистрирован",
                self.INSUFFICIENT_FOUNDS: "На счёте недостаточно средств",
                self.WEBHOOK_SIGNATURE_IS_INVALID: "Недействительная сигнатура",
                self.PRODUCT_NOT_FOUND: "Товар с таким ID не существует"
                }.get(self.error_code, "")


class InnerException(SanicException):
    status_code = 409
    message = "internal service error"

    def __init__(self, inner_error: InnerError):
        super().__init__(context={"error_code": inner_error.value,
                                  "error_name": inner_error.name,
                                  "error_message": inner_error.description})









