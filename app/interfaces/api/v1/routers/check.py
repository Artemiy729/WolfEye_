from fastapi import APIRouter, Request, HTTPException, status

from app.interfaces.api.v1.schemas.auth import CheckResponse

router = APIRouter(prefix="/check", tags=["check"])


@router.get("", response_model=CheckResponse)
def check_user(request: Request):
    """Защищенный эндпоинт для проверки пользователя"""
    # Middleware уже проверил аутентификацию и добавил пользователя в request.state
    return CheckResponse(id=request.state.current_user.id)
