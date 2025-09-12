from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.db.base import get_db
from app.interfaces.api.v1.schemas.auth import CheckResponse, User
from app.interfaces.api.v1.routers.auth import get_current_user

router = APIRouter(prefix="/check", tags=["check"])


@router.get("", response_model=CheckResponse)
def check_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Защищенный эндпоинт для проверки пользователя"""
    # В ТЗ указано возвращать id и email, но в модели User нет поля email
    # Возвращаем id и login вместо email
    return CheckResponse(
        id=current_user.id,
        email=current_user.login  # Используем login как email для соответствия ТЗ
    )
