from Crypto.Hash import SHA1


def get_signature_webhook(private_key: str, transaction_id: int,
                          user_id: int, bill_id: int, amount: id):
    signature = SHA1.new()
    signature.update(f"{private_key}:{transaction_id}:{user_id}:{bill_id}:{amount}".encode())
    signature = signature.hexdigest()
    return signature


if __name__ == "__main__":
    hook = get_signature_webhook(private_key="32CiTf_FDqF4_DJ3D",
                                 transaction_id=1244,
                                 user_id=555,
                                 bill_id=5550,
                                 amount=999)
    print(hook)
