from sanic import Sanic, response
from sanic_ext import openapi
from contextvars import ContextVar
import asyncio
import uvloop
from app.api.auth.routers import auth_router
from app.api.store.routers import store_router
from app.api.payment.routers import payment_router
from app.api.admin.routers import admin_router

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.models import Base

from app.middlewares import setup_db_middlewares

from .config_reader import config

app = Sanic(name="StoreApp")
app.ext.config.CORS = False
app.ext.config.OAS_URL_PREFIX = "/api"
app.ext.config.OAS_UI_DEFAULT = "swagger"
app.ext.openapi.describe(
    title="StoreAPI", version="1.0",
    description="Store API - Sanic Framework"
)
app.ext.openapi.build(app)
app.blueprint(blueprint=auth_router)
app.blueprint(blueprint=store_router)
app.blueprint(blueprint=payment_router)
app.blueprint(blueprint=admin_router)

@app.listener('after_server_start')
async def initial_db_session(app, loop):
    print(config.POSTGRES_USER, config.POSTGRES_HOST, config.POSTGRES_DB)
    engine = create_async_engine(
        f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}"
        f"@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}",
        echo=True
    )
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    _sessionmaker = sessionmaker(engine, AsyncSession, expire_on_commit=False)
    _base_model_session_ctx = ContextVar("session")

    await setup_db_middlewares(app=app,
                               sessionmaker=_sessionmaker,
                               base_model_session_ctx=_base_model_session_ctx)


if __name__ == "__main__":
    app.run(host=config.APP_HOST, port=config.APP_PORT)
