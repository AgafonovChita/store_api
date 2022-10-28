from sanic import response
from sanic.request import Request
from app.utils.jwt import check_token
from app.db.models import User
from app.services.repo import SQLAlchemyRepo, UserRepo


def token_validator(func):
    """ Функция-декоратор для проверки у пользователя прав доступа к endpoint """
    async def wrapped(request: Request):
        check = await check_token(token=request.headers.get("Authorization"))
        if check.get("status") == "error":
            return response.json(check, status=401)

        repo: SQLAlchemyRepo = request.ctx.repo
        user = await repo.get_repo(UserRepo).get_user_by_id(user_id=check.get("payload").get("user_id"))
        request.ctx.user = user
        result = await func(request=request)
        return result
    return wrapped


def user_validator(is_active: bool = True, is_admin: bool = False):
    """
    Функция-декоратор для проверки у пользователя прав доступа к endpoint

    :param is_active: активированный аккаунт
    :param is_admin: является ли пользователь админом
    """
    def validator(func):
        async def wrapped(request: Request):
            repo: SQLAlchemyRepo = request.ctx.repo
            user: User = await repo.get_repo(UserRepo).get_user_by_id(user_id=request.ctx.user.id)
            if is_active and not user.is_active:
                return response.json(status=401, body={"message": "user not activated"})

            if is_admin and not user.is_admin:
                return response.json(status=403)

            result = await func(request)

            return result
        return wrapped
    return validator

