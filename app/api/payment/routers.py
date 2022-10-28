from sanic import Blueprint, response
from sanic.request import Request
from sanic_pydantic import webargs
from app.api.payment.schemas import PaymentBody

from app.services import token_validator, user_validator
from app.services.repo import SQLAlchemyRepo, StoreRepo

payment_router = Blueprint(name="payment",
                           url_prefix="/payment")


@payment_router.post("/webhook")
@webargs(body=PaymentBody)
async def buy_product(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    payment_data: PaymentBody = PaymentBody.parse_raw(request.body)


