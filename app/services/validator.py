def token_validator(func):
    async def validator(request: Request):
        check = await check_token(token=request.headers.get("Authorization"))
        if check.get("status") == "error":
            return response.json(check, status=401)

        repo: SQLAlchemyRepo = request.ctx.repo
        user = await repo.get_repo(UserRepo).get_user_by_id(user_id=check.get("payload").get("user_id"))
        request.ctx.user = user
        result = await func(request=request)
        return result
    return validator