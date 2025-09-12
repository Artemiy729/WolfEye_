from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Optional

from app.infrastructure.db.base import get_db
from app.interfaces.api.v1.schemas.auth import LoginRequest, LoginResponse, RefreshRequest, RefreshResponse, User
from app.infrastructure.security.jwt import create_access_token, create_refresh_token, verify_token, verify_refresh_token

router = APIRouter(prefix="/auth", tags=["authentication"])

# Конфигурация безопасности
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хеширование пароля"""
    return pwd_context.hash(password)


def get_user_by_login(db: Session, login: str) -> Optional[User]:
    """Получение пользователя по логину"""
    from app.infrastructure.db.user_repository import get_user_by_login as get_user_from_db
    return get_user_from_db(db, login)


def authenticate_user(db: Session, login: str, password: str) -> Optional[User]:
    """Аутентификация пользователя"""
    user = get_user_by_login(db, login)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user




async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Получение текущего пользователя из токена"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    if not payload:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Используем SQLAlchemy модель UserModel, а не Pydantic модель User
    from app.infrastructure.db.user_repository import UserModel
    user_model = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user_model is None:
        raise credentials_exception
    
    # Конвертируем SQLAlchemy модель в Pydantic модель
    user = User(
        id=user_model.id,
        login=user_model.login,
        email=user_model.email,
        password_hash=user_model.password_hash
    )
    return user


@router.post("/login", response_model=LoginResponse)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Вход пользователя (JSON)"""
    user = authenticate_user(db, login_data.login, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }



@router.post("/refresh", response_model=RefreshResponse)
def refresh_token(refresh_data: RefreshRequest, db: Session = Depends(get_db)):
    """Обновление access токена"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_refresh_token(refresh_data.refresh_token)
    if not payload:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Используем SQLAlchemy модель UserModel
    from app.infrastructure.db.user_repository import UserModel
    user_model = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user_model is None:
        raise credentials_exception
    
    # Конвертируем SQLAlchemy модель в Pydantic модель
    user = User(
        id=user_model.id,
        login=user_model.login,
        email=user_model.email,
        password_hash=user_model.password_hash
    )
    
    access_token = create_access_token(user)
    
    return {"access_token": access_token}


