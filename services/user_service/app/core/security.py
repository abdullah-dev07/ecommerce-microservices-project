from passlib.context import CryptContext

# bcrypt is the industry-standard for password hashing.
# `deprecated="auto"` lets us upgrade algorithms later without breaking existing hashes.
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return _pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return _pwd_context.verify(plain, hashed)
