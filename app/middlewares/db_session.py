from sanic import Sanic
from app.services.repo import SQLAlchemyRepo, UserRepo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import sessionmaker
from contextvars import ContextVar


async def setup_db_middlewares(app: Sanic, maker: sessionmaker):
    @app.on_request
    async def inject_session(request):
        request.ctx.session = maker()
        request.ctx.repo = SQLAlchemyRepo(request.ctx.session)

        request.ctx.session_ctx_token = ContextVar("session").set(request.ctx.session)
        request.ctx.repo_ctx_token = ContextVar("repo").set(request.ctx.repo)

    @app.on_response()
    async def close_session(request, response):
        if hasattr(request.ctx, "session_ctx_token"):
            ContextVar("session").reset(request.ctx.session_ctx_token)
            await request.ctx.session.close()
        if hasattr(request.ctx, "repo_ctx_token"):
            ContextVar("repo").reset(request.ctx.repo_ctx_token)
