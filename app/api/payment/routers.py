from sanic import Blueprint, response
from sanic.request import Request
from sanic_ext.extensions.openapi.definitions import Response
from sanic_ext import openapi
from app.utils.validators import body_validator
from app.api.payment.schemas import PaymentSchema

from app.utils import webhook_signature_validator
from app.services.repo import SQLAlchemyRepo, TransactionRepo

payment_router = Blueprint(name="payment", url_prefix="/payment")


@payment_router.post("/webhook")
@openapi.definition(
    body={"application/json": PaymentSchema.schema()},
    response=Response(str, status=200),
    summary="Пополнение кошелька пользователя со стороннего сервиса",
    description="""private_key – приватный ключ, задаётся в свойствах приложения,
    transaction_id – уникальный идентификатор транзакции, user_id – пользователь на чей
    счёт произойдёт зачисление, bill_id – идентификатор счёта (если счёта с таким ID не
    существует, то счёт будет создан), amount – сумма транзакции.""",
)
@webhook_signature_validator
@body_validator(body_schema=PaymentSchema)
async def payment(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    schema: PaymentSchema = request.ctx.schema
    wallet = await repo.get_repo(TransactionRepo).payment_transaction(
        transaction_id=schema.transaction_id,
        amount=schema.amount,
        wallet_id=schema.bill_id,
        owner_id=schema.user_id)
    return response.json(wallet.to_dict())
