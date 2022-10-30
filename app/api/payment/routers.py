from sanic import Blueprint, response
from sanic.request import Request
from sanic_ext.extensions.openapi.definitions import RequestBody, Response, Parameter
from sanic_ext import openapi
from sanic_pydantic import webargs
from app.api.payment.schemas import PaymentSchema

from app.services import webhook_signature_validator
from app.services.repo import SQLAlchemyRepo, StoreRepo, TransactionRepo

payment_router = Blueprint(name="payment",
                           url_prefix="/payment")


@payment_router.post("/webhook")
@openapi.definition(
    body={'application/json': PaymentSchema.schema()},
    response=Response(str, status=200),
    summary="Пополнение кошелька пользователя со стороннего сервиса",
    description="""private_key – приватный ключ, задаётся в свойствах приложения,
    transaction_id – уникальный идентификатор транзакции, user_id – пользователь на чей
    счёт произойдёт зачисление, bill_id – идентификатор счёта (если счёта с таким ID не
    существует, то счёт будет создан), amount – сумма транзакции.""")
@webhook_signature_validator
@webargs(body=PaymentSchema)
async def buy_product(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    payment_data: PaymentSchema = PaymentSchema.parse_raw(request.body)
    await repo.get_repo(TransactionRepo). \
        payment_transaction(transaction_id=payment_data.transaction_id,
                            amount=payment_data.amount, wallet_id=payment_data.bill_id,
                            owner_id=payment_data.user_id)
    return response.text("wallet replenished", status=200)
