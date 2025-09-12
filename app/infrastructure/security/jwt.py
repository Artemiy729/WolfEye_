import jwt
from datetime import datetime, timedelta
from app.interfaces.api.v1.schemas.auth import User

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_EXPIRE_MINUTES = 15
REFRESH_EXPIRE_DAYS = 7

def create_access_token(user: User) -> str:
    expire = datetime.now() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    payload = {"sub": str(user.id), "email": user.email, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user: User) -> str:
    expire = datetime.now() + timedelta(days=REFRESH_EXPIRE_DAYS)
    payload = {"sub": str(user.id), "type": "refresh", "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None

def verify_refresh_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") == "refresh":
            return payload
        return None
    except jwt.PyJWTError:
        return None