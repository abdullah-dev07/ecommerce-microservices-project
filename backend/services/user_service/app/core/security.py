import base64
import hashlib

import bcrypt

# bcrypt has a hard 72-byte limit on its input. To support arbitrarily long
# passwords without truncation (and without the abandoned passlib library), we
# pre-hash the password with SHA-256 and base64-encode the digest. The result
# is always 44 ASCII bytes, well under bcrypt's limit, and base64 guarantees no
# embedded NUL bytes (which bcrypt would otherwise treat as a string terminator).


def _prehash(password: str) -> bytes:
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.b64encode(digest)


def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(_prehash(password), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(_prehash(plain), hashed.encode("utf-8"))
