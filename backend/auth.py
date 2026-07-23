import hashlib
from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import HTTPException, status
from jose import JWTError, jwt

SECRET_KEY = "change-me-in-production-use-a-long-random-string"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 2
REFRESH_TOKEN_EXPIRE_DAYS = 5


def hash_password(password: str) -> str:
    prehashed = hashlib.sha256(password.encode()).hexdigest().encode()
    return bcrypt.hashpw(prehashed, bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    prehashed = hashlib.sha256(plain.encode()).hexdigest().encode()
    return bcrypt.checkpw(prehashed, hashed.encode())


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    payload = {"sub": subject, "type": "access", "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": subject, "type": "refresh", "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )