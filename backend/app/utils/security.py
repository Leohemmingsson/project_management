from passlib.hash import bcrypt


def hash_password(password: str) -> str:
    """
    Hashing password
    """
    return bcrypt.hash(password)

def is_password_correct(password: str, hashed_password: str) -> bool:
    """
    Checks if password is correct
    """
    return bcrypt.verify(password, hashed_password)
