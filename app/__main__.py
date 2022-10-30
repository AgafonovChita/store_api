from sanic import Sanic, response
from sanic_ext import Config
from contextvars import ContextVar
import pendulum
from app.api.auth.routers import auth_router
from app.api.store.routers import store_router
from app.api.payment.routers import payment_router
from app.api.admin.routers import admin_router

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.models import Base
from app.services.repo import SQLAlchemyRepo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.middlewares import setup_db_middlewares
from app.utils.token_clean import token_clean
from .config_reader import config



app = Sanic(name="StoreApp")
app.extend(config=Config(oas_autodoc=True, oas_ui_default="swagger" ,cors=False))
app.ext.openapi.describe(
    title="StoreAPI", version="1.0",
    description="Store API - Sanic Framework"
)
app.blueprint(blueprint=auth_router)
app.blueprint(blueprint=store_router)
app.blueprint(blueprint=payment_router)
app.blueprint(blueprint=admin_router)


async def initial_db_session():
    engine = create_async_engine(
        f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}"
        f"@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}",
        echo=True)
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    _sessionmaker = sessionmaker(engine, AsyncSession, expire_on_commit=False)
    await setup_db_middlewares(app=app, maker=_sessionmaker)
    return _sessionmaker


async def initial_scheduler(maker):
    scheduler = AsyncIOScheduler(timezone="Europe/Berlin")
    date_start = pendulum.now().add(seconds=30)
    scheduler.add_job(token_clean, 'date',
                      run_date=date_start,
                      kwargs={"repo": SQLAlchemyRepo(maker())})
    scheduler.start()


@app.listener('after_server_start')
async def initial_db_session(app, loop):
    _session_maker = await initial_db_session()
    initial_scheduler()


if __name__ == "__main__":
    app.run(host=config.APP_HOST, port=config.APP_PORT)
