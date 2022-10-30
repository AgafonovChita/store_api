from sanic import response
from sanic.request import Request
from app.utils.jwt import check_token
from app.db.models import User
from app.services.repo import SQLAlchemyRepo, UserRepo
from app.api.payment.schemas import PaymentSchema
from app.utils.crypt import get_signature_webhook
from app.config_reader import config


def token_validator(func):
    """
    Функция-декоратор.
    Позволяет проверить наличие токена в заголовке Authorization и его валидность.
    Работает с обработчиками, принимающими объект Request.
    В случае у спеха в request.ctx.user будет помещён объект User.
    """

    async def wrapped(request: Request, *args, **kwargs):
        check = await check_token(token=request.headers.get("Authorization"))
        if check.get("status") == "error":
            return response.json(check, status=401)
        repo: SQLAlchemyRepo = request.ctx.repo
        user = await repo.get_repo(UserRepo).get_user_by_id(
            user_id=check.get("payload").get("user_id")
        )
        request.ctx.user = user
        result = await func(request=request, *args, **kwargs)
        return result

    return wrapped


def user_validator(is_active: bool = True, is_admin: bool = False):
    """
    Функция-декоратор.
    Позволяет проверить роль пользователя и активность его аккаунта.
    Работает с обработчиками, принимающими объект Request.
    Декоратор должен быть инициализирован после @token_validator.

    :param is_active: активированный аккаунт.
    :param is_admin: является ли пользователь админом.
    """

    def validator(func):
        async def wrapped(request: Request, *args, **kwargs):
            repo: SQLAlchemyRepo = request.ctx.repo
            # user: User = await repo.get_repo(UserRepo).get_user_by_id(user_id=request.ctx.user.id)
            user: User = request.ctx.user
            if is_active and not user.is_active:
                return response.json(status=401, body={"message": "user not activated"})

            if is_admin and not user.is_admin:
                return response.json(status=403)

            result = await func(request, *args, **kwargs)

            return result

        return wrapped

    return validator


def webhook_signature_validator(func):
    """
    Функция-декоратор.
    Позволяет проверить валидность signature у webhook, пришедшего на payload/webhook
    """

    async def wrapped(request: Request, *args, **kwargs):
        payment_data: PaymentSchema = PaymentSchema.parse_raw(request.body)
        signature = await get_signature_webhook(
            private_key=config.PRIVATE_KEY,
            amount=payment_data.amount,
            transaction_id=payment_data.transaction_id,
            user_id=payment_data.user_id,
            bill_id=payment_data.bill_id,
        )
        if signature != payment_data.signature:
            return response.json(
                body={"message": "signature webhook invalid"}, status=400
            )
        return await func(request, *args, **kwargs)

    return wrapped
