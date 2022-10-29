from sanic import Blueprint, response, HTTPResponse

from sanic.request import Request
from sanic_pydantic import webargs
from app.api.payment.schemas import PaymentBody
from app.services import token_validator, user_validator
from app.services.repo import SQLAlchemyRepo, StoreRepo, TransactionRepo, AdminRepo
from .schemas import UserStatusBody, AddProductBody, EditProductBody, DeleteProductBody

admin_router = Blueprint(name="admin",
                         url_prefix="/admin")



@admin_router.get("/products")

@token_validator
@user_validator(is_active=True, is_admin=True)
async def get_products(request: Request, **kwargs) -> HTTPResponse:
    repo: SQLAlchemyRepo = request.ctx.repo
    resp = [prod.to_dict() for prod in await repo.get_repo(StoreRepo).get_products()]
    return response.json(resp)


@admin_router.route("/users_and_wallets", methods=["POST", "GET"])
@token_validator
@user_validator(is_active=True, is_admin=True)
async def get_users_and_wallets(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    user_and_wallets_list = [dict(uw).get("row_to_json") for uw in
                             await repo.get_repo(AdminRepo).get_users_and_wallets()]
    return response.json(user_and_wallets_list)


@admin_router.route("/users", methods=["POST", "GET"])
@token_validator
@user_validator(is_active=True, is_admin=True)
async def get_users(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    user_list = [dict(user) for user in await repo.get_repo(AdminRepo).get_users()]
    return response.json(user_list)


@admin_router.get("/user/<user_id>")
@token_validator
@user_validator(is_active=True, is_admin=True)
async def get_users(request: Request, user_id: int, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    user = await repo.get_repo(AdminRepo).get_user_by_id(user_id=int(user_id))
    return response.json(user.to_dict())


@admin_router.post("/change_user_status")
@token_validator
@user_validator(is_active=True, is_admin=True)
@webargs(body=UserStatusBody)
async def get_users(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    user_status: UserStatusBody = UserStatusBody.parse_raw(request.body)
    await repo.get_repo(AdminRepo).change_user_status(user_id=user_status.user_id,
                                                      is_active=user_status.is_active, is_admin=user_status.is_admin)
    return response.json(body={"message": f"User {user_status.user_id} - "
                                          f"is_active:{user_status.is_active} - "
                                          f"if_admin:{user_status.is_admin}"},
                         status=200)


@admin_router.post("/add_product")
@token_validator
@user_validator(is_active=True, is_admin=True)
@webargs(body=AddProductBody)
async def get_users(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    product_body: AddProductBody = AddProductBody.parse_raw(request.body)
    await repo.get_repo(AdminRepo).add_new_product(header=product_body.header, description=product_body.description,
                                                   price=product_body.price)
    return response.json(body={"message": f"Product '{product_body.header}' added"},
                         status=200)


@admin_router.post("/edit_product")
@token_validator
@user_validator(is_active=True, is_admin=True)
@webargs(body=EditProductBody)
async def get_users(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    product_body: EditProductBody = EditProductBody.parse_raw(request.body)
    await repo.get_repo(AdminRepo).edit_product(product_id=product_body.product_id, header=product_body.header,
                                                description=product_body.description, price=product_body.price)
    return response.json(body={"message": f"Product '{product_body.header}' edited"},
                         status=200)


@admin_router.post("/delete_product")
@token_validator
@user_validator(is_active=True, is_admin=True)
@webargs(body=DeleteProductBody)
async def get_users(request: Request, **kwargs):
    repo: SQLAlchemyRepo = request.ctx.repo
    product_body: DeleteProductBody = DeleteProductBody.parse_raw(request.body)
    await repo.get_repo(AdminRepo).delete_product(product_id=product_body.product_id)
    return response.json(body={"message": f"Product '{product_body.product_id}' deleted"},
                         status=200)

