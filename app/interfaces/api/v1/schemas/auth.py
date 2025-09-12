from pydantic import BaseModel


class LoginRequest(BaseModel):
    login: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str


class CheckResponse(BaseModel):
    id: str
    email: str


class User(BaseModel):
    id: str
    login: str
    email: str
    password_hash: str
