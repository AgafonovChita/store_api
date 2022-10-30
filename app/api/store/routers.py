from sanic import Blueprint, response
from sanic.request import Request
from typing import List
from sanic_ext.extensions.openapi.definitions import RequestBody, Response, Parameter
from sanic_pydantic import webargs
from app.api.store.schemas import BuyBody, ProductSchema, WalletSchema
from sanic_ext import openapi

from app.services import token_validator, user_validator
from app.services.repo import SQLAlchemyRepo, StoreRepo

store_router = Blueprint(name="store", url_prefix="/store")


@store_router.post("/products")
@openapi.definition(
    parameter=Parameter("Authorization", str, "header"),
    summary="Получить список всех товаров",
    response=Response({"application/json": List[ProductSchema]}, status=200),
    description="",
)
@token_validator
@user_validator(is_active=True)
async def get_products(request: Request):
    repo: SQLAlchemyRepo = request.ctx.repo
    resp = [prod.to_dict() for prod in await repo.get_repo(StoreRepo).get_products()]
    return response.json(resp)


@store_router.post("/wallets")
@openapi.definition(
    parameter=Parameter("Authorization", str, "header"),
    summary="Получить список своих кошельков",
    response=Response({"application/json": List[WalletSchema]}, status=200),
    description="Пользователь получает список кошельков, принадлежащих ему. "
    "Идентификация пользователя происходит через access-token.",
)
@token_validator
@user_validator(is_active=True)
async def get_wallets(request: Request):
    repo: SQLAlchemyRepo = request.ctx.repo
    resp = [
        dict(wallet)
        for wallet in await repo.get_repo(StoreRepo).get_wallets(
            user_id=request.ctx.user.id
        )
    ]
    return response.json(resp)


@store_router.post("/buy_product")
@openapi.definition(
    body={"application/json": BuyBody.schema()},
    parameter=Parameter("Authorization", str, "header"),
    summary="Купить товар",
    response=Response(str, status=200),
    description="Денежные средства списываются со счёта, указанного пользователем в теле-запроса",
)
@token_validator
@user_validator(is_active=True)
@webargs(body=BuyBody)
async def buy_product(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    buy_data: BuyBody = BuyBody.parse_raw(request.body)

    if not await repo.get_repo(StoreRepo).check_ability_to_pay(
        wallet_id=buy_data.wallet_id, product_id=buy_data.product_id
    ):
        return response.json(
            body={"status": "error", "message": "Недостаточно средств на балансе счёта"}
        )

    await repo.get_repo(StoreRepo).buy_product(
        wallet_id=buy_data.wallet_id, product_id=buy_data.product_id
    )
    return response.text("product purchased", status=200)
