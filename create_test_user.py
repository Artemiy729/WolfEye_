import uuid
from app.infrastructure.db.base import SessionLocal
from app.infrastructure.db.user_repository import UserModel
from app.interfaces.api.v1.routers.auth import get_password_hash

"""
Скрипт для создания тестового пользователя
"""
def create_test_user():
    """Создает тестового пользователя"""
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже пользователь
        existing_user = db.query(UserModel).filter(UserModel.login == "test").first()
        if existing_user:
            print("Пользователь 'test' уже существует!")
            return
        
        # Создаем нового пользователя
        user = UserModel(
            id=str(uuid.uuid4()),
            login="test",
            email="test@example.com",
            password_hash=get_password_hash("test123")
        )
        
        db.add(user)
        db.commit()
    
        print("Тестовый пользователь создан успешно!")
        print("Логин: test")
        print("Пароль: test123")
        print("Email: test@example.com")
        
    except Exception as e:
        print(f"Ошибка при создании пользователя: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
