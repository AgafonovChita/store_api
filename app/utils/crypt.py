import bcrypt
from Crypto.Hash import SHA1


async def crypt_password(password: str) -> "str_hash":
    """hash password + salt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


async def check_password(password: str, hash_password: str) -> bool:
    """check valid auth password"""
    return bcrypt.checkpw(password.encode(), hash_password)


async def get_signature_webhook(private_key: str, transaction_id: int,
                                user_id: int, bill_id: int, amount: id):
    signature = SHA1.new()
    signature.update(
        f"{private_key}:{transaction_id}:{user_id}:{bill_id}:{amount}".encode()
    )
    signature = signature.hexdigest()
    return signature
