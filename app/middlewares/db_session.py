from sanic import Sanic
from app.services.repo import SQLAlchemyRepo, UserRepo


async def setup_db_middlewares(app: Sanic,
                               sessionmaker, base_model_session_ctx):
    @app.on_request
    async def inject_session(request):
        request.ctx.session = sessionmaker()
        request.ctx.repo = SQLAlchemyRepo(request.ctx.session)
        request.ctx.session_ctx_token = base_model_session_ctx.set(request.ctx.session)
        request.ctx.repo_ctx_token = base_model_session_ctx.set(request.ctx.repo)

    @app.on_response()
    async def close_session(request, response):
        if hasattr(request.ctx, "session_ctx_token"):
            base_model_session_ctx.reset(request.ctx.session_ctx_token)
            await request.ctx.session.close()
        if hasattr(request.ctx, "repo_ctx_token"):
            base_model_session_ctx.reset(request.ctx.repo_ctx_token)

