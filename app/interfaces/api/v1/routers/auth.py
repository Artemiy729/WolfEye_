from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.db.base import get_db
from app.interfaces.api.v1.schemas.auth import LoginRequest, LoginResponse, RefreshRequest, RefreshResponse
from app.infrastructure.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])



@router.post("/login", response_model=LoginResponse)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Вход пользователя (JSON)"""
    auth_service = AuthService(db)
    
    tokens = auth_service.authenticate_user(login_data.login, login_data.password)
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return tokens


@router.post("/refresh", response_model=RefreshResponse)
def refresh_token(refresh_data: RefreshRequest, db: Session = Depends(get_db)):
    """Обновление access токена"""
    auth_service = AuthService(db)
    
    access_token = auth_service.refresh_access_token(refresh_data.refresh_token)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"access_token": access_token}


