import bcrypt


async def crypt_password(password: str) -> "str_hash":
    """hash password + salt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


async def check_password(password: str, hash_password: str) -> bool:
    """check valid auth password"""
    return bcrypt.checkpw(password.encode(), hash_password)

