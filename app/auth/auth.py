from sanic import Blueprint

auth_router = Blueprint(
    url_prefix="/auth"
)

@auth_router.post("/register")
async def register_new_user():

