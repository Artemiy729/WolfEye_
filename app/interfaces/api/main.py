from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from app.interfaces.api.v1.routers import auth, check

app = FastAPI(
    title="WolfEye API",
    description="API для анализа резюме",
    version="1.0.0"
)

# # Настройка CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # В продакшене указать конкретные домены
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(auth.router)
app.include_router(check.router)


@app.get("/")
def read_root():
    """Корневой эндпоинт"""
    return {"message": "WolfEye API is running"}


@app.get("/health")
def health_check():
    """Проверка здоровья API"""
    return {"status": "healthy"}