from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import timedelta, datetime
from service.items_services.items import UserItem
import uuid

import jwt

from core import settings


ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'
TOKEN_TYPE_FIELD = 'type'


@dataclass(frozen=True)
class JWT:
    """Класс для создания JWT токена, а также его декодирование"""
    private_key: str = settings.auth.private_key.read_text()
    public_key: str = settings.auth.public_key.read_text()
    algorithm: str = settings.auth.algorithm

    def encode_jwt(
        self,
        payload: dict,
        expire_minutes: int
    ) -> str:
        """JWT создание токена:
        payload -> объект данных пользователя
        expire_minutes -> время жизни токена"""

        to_encode = payload.copy()
        now = datetime.now()
        exp = now + timedelta(minutes=expire_minutes)
        jti = str(uuid.uuid4())

        to_encode.update(
            exp=exp,   # время окончания жизни токена
            iat=now,   # время создания токена
            jti=jti    # уникальный идентификатор токена
        )

        encoded = jwt.encode(
            to_encode,
            self.private_key,
            algorithm=self.algorithm
        )
        return encoded

    def decode_jwt(
        self,
        token: str | bytes,
    ) -> Dict[str, Any]:
        """JWT декодирование"""
        decoded = jwt.decode(
            token,
            self.public_key,
            algorithms=[self.algorithm]
        )
        return decoded

    def create_token(
        self,
        token_type: str,
        token_data: dict,
        expire_minutes: int
    ) -> str:
        jwt_payload = {TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(token_data)
        return self.encode_jwt(
            payload=jwt_payload,
            expire_minutes=expire_minutes
        )

    def create_access_token(self, user_id: int) -> str: # for accepting user: UserItem middleware should have access to DB (i used uow)
        jwt_payload = {
            'sub': str(user.id)
        }
        return self.create_token(
            ACCESS_TOKEN_TYPE,
            jwt_payload,
            settings.auth.access_token_expire_minutes
        )

    def create_refresh_token(self, user_id: int) -> str: # for accepting user: UserItem middleware should have access to DB (i used uow). UserItem makes sense if u wanna add more fields than just id to token
        jwt_payload = {
            'sub': str(user.id),
        }
        return self.create_token(
            REFRESH_TOKEN_TYPE,
            jwt_payload,
            settings.auth.refresh_token_expire_minutes
        )



jwt_processes = JWT()


__all__ = ['jwt_processes']