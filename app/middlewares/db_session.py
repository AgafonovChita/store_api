from sanic import Sanic
from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from app.services.repo import SQLAlchemyRepo
from app.db.base import Base


def setup_db_middlewares(app: Sanic, engine: AsyncEngine):
    _base_model_session_ctx = ContextVar("session")

    @app.after_server_start
    async def init_models(app, loop):
        async with engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @app.on_request
    async def inject_session(request):
        request.ctx.session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)()
        request.ctx.repo = SQLAlchemyRepo(request.ctx.session)
        request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)

    @app.on_response
    async def close_session(request, response):
        if hasattr(request.ctx, "session_ctx_token"):
            _base_model_session_ctx.reset(request.ctx.session_ctx_token)
            await request.ctx.session.close()
