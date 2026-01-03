import bcrypt


def hash_psw(
    password: str,
) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def check_psw(password: str, pwd_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password=pwd_hash.encode())
