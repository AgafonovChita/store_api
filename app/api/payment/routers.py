from sanic import Blueprint, response
from sanic.request import Request
from sanic_pydantic import webargs
from app.api.payment.schemas import PaymentBody

from app.services import webhook_signature_validator
from app.services.repo import SQLAlchemyRepo, StoreRepo, TransactionRepo

payment_router = Blueprint(name="payment",
                           url_prefix="/payment")


@payment_router.post("/webhook")
@webhook_signature_validator(check_signature=False)
@webargs(body=PaymentBody)
async def buy_product(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    payment_data: PaymentBody = PaymentBody.parse_raw(request.body)
    await repo.get_repo(TransactionRepo). \
        payment_transaction(transaction_id=payment_data.transaction_id,
                            amount=payment_data.amount, wallet_id=payment_data.bill_id,
                            owner_id=payment_data.user_id)
    return response.json(body={"message": "wallet replenished"}, status=200)
