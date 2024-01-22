from jose import jwt
from passlib.context import CryptContext
from .config import SECRET_KEY, EXP_DATE, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(username: str) -> str:
    return jwt.encode(claims={"sub": username, "exp": EXP_DATE}, key=SECRET_KEY, algorithm=ALGORITHM)
