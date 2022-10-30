from sanic import Blueprint, response, HTTPResponse
from typing import List
from sanic.request import Request
from sanic_pydantic import webargs
from sanic_ext import openapi
from sanic_ext.extensions.openapi.definitions import RequestBody, Response, Parameter
from app.api.payment.schemas import PaymentSchema
from app.api.store.schemas import ProductSchema
from app.api.admin.schemas import UserAndWalletSchema, UserSchema
from app.services import token_validator, user_validator
from app.services.repo import SQLAlchemyRepo, StoreRepo, TransactionRepo, AdminRepo
from .schemas import UserStatusSchema, AddProductSchema, EditProductSchema, DeleteProductSchema

admin_router = Blueprint(name="admin",
                         url_prefix="/admin")


@admin_router.get("/products")
@openapi.definition(
    parameter=Parameter("Authorization", str, "header"),
    summary="Получить список всех товаров",
    response=Response({"application/json": List[ProductSchema]}, status=200))
@token_validator
@user_validator(is_active=True, is_admin=True)
async def get_products(request: Request, **kwargs) -> HTTPResponse:
    repo: SQLAlchemyRepo = request.ctx.repo
    resp = [prod.to_dict() for prod in await repo.get_repo(StoreRepo).get_products()]
    return response.json(resp)


@admin_router.route("/users_and_wallets", methods=["POST", "GET"])
@openapi.definition(
    parameter=Parameter("Authorization", str, "header"),
    summary="Получить список всех пользователей и их кошельков",
    response=Response({"application/json": List[UserAndWalletSchema]}, status=200),
    description="Выполнение запроса возможно только с аккаунта администратора")
@token_validator
@user_validator(is_active=True, is_admin=True)
async def get_users_and_wallets(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    user_and_wallets_list = [dict(uw).get("row_to_json") for uw in
                             await repo.get_repo(AdminRepo).get_users_and_wallets()]
    return response.json(user_and_wallets_list)


@admin_router.route("/users", methods=["POST", "GET"])
@openapi.definition(
    parameter=Parameter("Authorization", str, "header"),
    summary="Получить список всех пользователей",
    response=Response({"application/json": List[UserSchema]}, status=200),
    description="Выполнение запроса возможно только с аккаунта администратора")
@token_validator
@user_validator(is_active=True, is_admin=True)
async def get_users(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    user_list = [dict(user) for user in await repo.get_repo(AdminRepo).get_users()]
    return response.json(user_list)


@admin_router.get("/user/<user_id>")
@openapi.parameter("user_id")
@openapi.definition(
    parameter=Parameter("Authorization", str, "header"),
    summary="Получить данные пользователя по ID",
    response=Response({"application/json": UserSchema}, status=200),
    description="Выполнение запроса возможно только с аккаунта администратора")
@token_validator
@user_validator(is_active=True, is_admin=True)
async def get_users(request: Request, user_id: int, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    user = await repo.get_repo(AdminRepo).get_user_by_id(user_id=int(user_id))
    return response.json(user.to_dict())


@admin_router.post("/change_user_status")
@openapi.definition(
    body={'application/json': UserStatusSchema.schema()},
    parameter=Parameter("Authorization", str, "header"),
    summary="Изменить статус пользователя (is_active, is_admin)",
    response=Response({"application/json": UserStatusSchema.schema()}, status=200),
    description="Выполнение запроса возможно только с аккаунта администратора")
@token_validator
@user_validator(is_active=True, is_admin=True)
@webargs(body=UserStatusSchema)
async def get_users(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    user_status: UserStatusSchema = UserStatusSchema.parse_raw(request.body)
    await repo.get_repo(AdminRepo).change_user_status(user_id=user_status.user_id,
                                                      is_active=user_status.is_active, is_admin=user_status.is_admin)
    return response.json(body={"user_id": {user_status.user_id},
                               "is_active": {user_status.is_active},
                               "is_admin": {user_status.is_admin}}, status=200)


@admin_router.post("/add_product")
@openapi.definition(
    body={'application/json': AddProductSchema.schema()},
    parameter=Parameter("Authorization", str, "header"),
    summary="Добавить новый товар",
    response=Response(response.text, status=200, description="Подтверждение добавления товара"),
    description="Выполнение запроса возможно только с аккаунта администратора")
@token_validator
@user_validator(is_active=True, is_admin=True)
@webargs(body=AddProductSchema)
async def edit_product(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    product_body: AddProductSchema = AddProductSchema.parse_raw(request.body)
    await repo.get_repo(AdminRepo).add_new_product(header=product_body.header, description=product_body.description,
                                                   price=product_body.price)
    return response.text(f"Product '{product_body.header}' added", status=200)


@admin_router.post("/edit_product")
@openapi.definition(
    body={'application/json': EditProductSchema.schema()},
    parameter=Parameter("Authorization", str, "header"),
    summary="Изменить товар по ID",
    response=Response(response.text, status=200, description="Подтверждение изменения товара"),
    description="Выполнение запроса возможно только с аккаунта администратора")
@token_validator
@user_validator(is_active=True, is_admin=True)
@webargs(body=EditProductSchema)
async def edit_product(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    product_body: EditProductSchema = EditProductSchema.parse_raw(request.body)
    await repo.get_repo(AdminRepo).edit_product(product_id=product_body.product_id, header=product_body.header,
                                                description=product_body.description, price=product_body.price)
    return response.text(f"Product '{product_body.header}' edited", status=200)


@admin_router.post("/delete_product")
@openapi.definition(
    body={'application/json': DeleteProductSchema.schema()},
    parameter=Parameter("Authorization", str, "header"),
    summary="Удалить товар по ID",
    response=Response(response.text, status=200, description="Подтверждение удаления товара"),
    description="Выполнение запроса возможно только с аккаунта администратора")
@token_validator
@user_validator(is_active=True, is_admin=True)
@webargs(body=DeleteProductSchema)
async def delete_product(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    product_body: DeleteProductSchema = DeleteProductSchema.parse_raw(request.body)
    await repo.get_repo(AdminRepo).delete_product(product_id=product_body.product_id)
    return response.text(f"Product '{product_body.product_id}' deleted", status=200)
