from sanic import Blueprint, response
from sanic.response import redirect, text
from sanic.request import Request
from sanic_pydantic import webargs
from app.api.user import UserData
from app.db.models import User, Wallet
from app.utils.crypt import crypt_password, check_password
from app.services import token_validator
from app.config_reader import config
from app.services.repo import SQLAlchemyRepo, UserRepo
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.jwt import create_token, check_token

auth_router = Blueprint(name="auth",
                        url_prefix="/auth")


@auth_router.post("/register")
@webargs(body=UserData)
async def register_new_user(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    user_data = UserData.parse_raw(request.body)

    if not await repo.get_repo(UserRepo).check_user_by_login(login=user_data.login):
        user_data.password = await crypt_password(password=user_data.password)
        user = await repo.get_repo(UserRepo).user_registration(user_data=user_data)
        url = request.app.url_for("auth.activate_account", user_id=user.id,
                                  _scheme="http", _external=True,
                                  _server=f"{config.APP_HOST}:{config.APP_PORT}")
        return text(url, status=200)
    return response.json({"error": "this login already exists"}, status=401)


@auth_router.get('/activate/<user_id>')
async def activate_account(request, user_id: int):
    repo: SQLAlchemyRepo = request.ctx.repo
    if not await repo.get_repo(UserRepo).check_user_by_id(user_id=user_id):
        return response.json({"message": "user with this id is not registered"}, status=401)
    await repo.get_repo(UserRepo).activate_account(user_id=user_id)
    return response.json({"message": f"Account {user_id} successfully activated"}, status=200)


@auth_router.post("/login")
@webargs(body=UserData)
async def login_user(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    user_data: UserData = UserData.parse_raw(request.body)
    user = await repo.get_repo(UserRepo).get_user_by_login(login=user_data.login)

    if (not user) or (not await check_password(password=user_data.password, hash_password=user.password)):
        return response.json({"message": "user with this login-password is not registered"}, status=401)

    access_token = await create_token(user_id=user.id, type_token="access")
    refresh_token = await create_token(user_id=user.id, type_token="refresh")
    return response.json({"access_token": access_token,
                          "refresh_token": refresh_token}, status=200)



@auth_router.post("/refresh_token")
@token_validator
async def update_token(request: Request):
    access_token = await create_token(user_id=request.ctx.user.id, type_token="access")
    refresh_token = await create_token(user_id=request.ctx.user.id, type_token="refresh")
    return response.json({"access_token": access_token, "refresh_token": refresh_token}, status=200)

