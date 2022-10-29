from sanic import Blueprint, response
from sanic.request import Request
from sanic_pydantic import webargs
from app.api.store.schemas import BuyBody
import json
from app.api.auth import UserBody
from app.db.models import Product

from app.services import token_validator, user_validator
from app.services.repo import SQLAlchemyRepo, StoreRepo

from app.utils.crypt import crypt_password, check_password
from app.utils.jwt import create_token

from app.config_reader import config

store_router = Blueprint(name="store",
                         url_prefix="/store")


@store_router.post("/products")
@token_validator
@user_validator(is_active=True)
async def get_products(request: Request):
    repo: SQLAlchemyRepo = request.ctx.repo
    resp = [prod.to_dict() for prod in await repo.get_repo(StoreRepo).get_products()]
    return response.json(resp)


@store_router.post("/wallets")
@token_validator
@user_validator(is_active=True)
async def get_wallets(request: Request):
    repo: SQLAlchemyRepo = request.ctx.repo
    resp = [dict(wallet) for wallet in await repo.get_repo(StoreRepo).get_wallets(user_id=request.ctx.user.id)]
    return response.json(resp)


@store_router.post("/buy_product")
@token_validator
@user_validator(is_active=True)
@webargs(body=BuyBody)
async def buy_product(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    buy_data: BuyBody = BuyBody.parse_raw(request.body)

    if not await repo.get_repo(StoreRepo).check_ability_to_pay(wallet_id=buy_data.wallet_id, product_id=buy_data.product_id):
        return response.json(body={"status": "error", "message": "Недостаточно средств на балансе счёта"})

    await repo.get_repo(StoreRepo).buy_product(wallet_id=buy_data.wallet_id, product_id=buy_data.product_id)
    return response.json(body={}, status=200)


