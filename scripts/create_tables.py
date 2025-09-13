from app.infrastructure.db.base import Base, engine

def create_tables():
    """Создание всех таблиц в базе данных"""
    print("Создаем таблицы...")
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы успешно!")
    
    # Проверяем, что таблицы созданы
    from sqlalchemy import text
    with engine.connect() as conn:
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        tables = result.fetchall()
        print(f"Таблицы в БД: {[table[0] for table in tables]}")

if __name__ == "__main__":
    create_tables()
