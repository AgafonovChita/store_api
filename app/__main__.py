from sanic import Sanic

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
app.blueprint(blueprint=auth_router)
app.blueprint(blueprint=store_router)
app.blueprint(blueprint=payment_router)
app.blueprint(blueprint=admin_router)


async def initial_db_session():
    engine = create_async_engine(
        f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}"
        f"@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}",
        echo=True
    )
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    _sessionmaker = sessionmaker(engine, AsyncSession, expire_on_commit=False)
    _base_model_session_ctx = ContextVar("session")

    await setup_db_middlewares(app=app,
                               sessionmaker=_sessionmaker,
                               base_model_session_ctx=_base_model_session_ctx)


async def main():
    await initial_db_session()

    server = await app.create_server(
        port=config.APP_PORT, host=config.APP_HOST, return_asyncio_server=True
    )

    if server is None:
        return

    await server.startup()
    await server.serve_forever()


if __name__ == "__main__":
    asyncio.set_event_loop(uvloop.new_event_loop())
    asyncio.run(main())
