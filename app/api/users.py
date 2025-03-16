from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)

from sqlalchemy.ext.asyncio import AsyncSession

from core import settings
from core.db import db_core

from schemas.user import UserRead

from utils.jwt_process import jwt_processes

# создание роутера для api пользователя, импорт настроек префикса и тегов
router = APIRouter(
    prefix=settings.api.v1.users_prefix,
    tags=settings.api.v1.users_tags
)
oauth2password = OAuth2PasswordBearer(tokenUrl="auth/login")

fake_users_db = {
    "test@email.com": {
        "id": 1,
        "name": "ООО Ромашка",
        "email": "test@email.com",
        "password": "123456",
        "role": "company"
    }
}

@router.post("/auth/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(db_core.session_getter)
):
    # crud операции с аргументов session
    user = fake_users_db.get(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Неверные email или пароль")

    access_token = jwt_processes.encode_jwt(payload={"sub": user["id"], "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}