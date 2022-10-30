from sanic import Sanic
from sanic_ext import Config

from app.api.auth.routers import auth_router
from app.api.store.routers import store_router
from app.api.payment.routers import payment_router
from app.api.admin.routers import admin_router
from app.middlewares.db_session import setup_db_middlewares
from app.services.repo import SQLAlchemyRepo

from app.utils.token_clean import token_clean

from sqlalchemy.ext.asyncio import create_async_engine

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .config_reader import config


def init_app():
    app = Sanic("StoreAPP")
    app.extend(config=Config(oas_autodoc=True, oas_ui_default="swagger", cors=False))
    app.ext.openapi.describe(
        title="StoreAPI", version="1.0", description="Store API - Sanic Framework"
    )

    app.blueprint(blueprint=auth_router)
    app.blueprint(blueprint=store_router)
    app.blueprint(blueprint=payment_router)
    app.blueprint(blueprint=admin_router)

    engine = create_async_engine(
        f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}"
        f"@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}",
        echo=True,
    )

    setup_db_middlewares(app=app, engine=engine)

    @app.after_server_start
    async def create_sheduler(app, loop):
        app.ctx.scheduler = AsyncIOScheduler()
        app.ctx.scheduler.add_job(token_clean, "interval", args=[engine],
                                  seconds=config.INTERVAL_DELETE_EXPIRE_TOKENS)
        app.ctx.scheduler.start()

    return app


if __name__ == "__main__":
    init_app().run(host=config.APP_HOST, port=config.APP_PORT)
