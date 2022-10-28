from sanic import Blueprint, response
from sanic.request import Request
from sanic_pydantic import webargs
import json
from app.api.auth import UserData
from app.db.models import Product

from app.services import token_validator
from app.services.repo import SQLAlchemyRepo, StoreRepo

from app.utils.crypt import crypt_password, check_password
from app.utils.jwt import create_token

from app.config_reader import config


store_router = Blueprint(name="store",
                        url_prefix="/store")


@store_router.post("/products")
@token_validator
async def get_products(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    resp = [prod.to_dict() for prod in await repo.get_repo(StoreRepo).get_products()]
    return response.json(resp)


@store_router.post("/wallets")
@token_validator
async def get_wallets(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    resp = [wallet.to_dict() for wallet in await repo.get_repo(StoreRepo).get_wallets(user_id=request.ctx.user.id)]
    return response.json(resp)


