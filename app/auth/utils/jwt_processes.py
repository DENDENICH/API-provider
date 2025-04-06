from typing import Optional, Dict
from dataclasses import dataclass
from datetime import timedelta, datetime

import jwt

from core import settings


@dataclass(frozen=True)
class JWT:
    """Класс для создания JWT токена, а также его декодирование"""
    private_key: str = settings.auth.private_key.read_text()
    public_key: str = settings.auth.public_key.read_text()
    algorithm: str = settings.auth.algorithm
    access_token_expire_hours: int = settings.auth.access_token_expire_hours

    def encode_jwt(
            self,
            payload: dict,
            expire_timedelta: timedelta | None = None
    ) -> str:
        """JWT создание токена:
        payload -> объект данных пользователя
        expire_timedelta -> время жизни токена"""

        to_encode = payload.copy()
        now = datetime.now()

        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(
                hours=self.access_token_expire_hours
            )

        to_encode.update(
            exp=expire, # time when the token expires
            iat=now # time when the token create
        )
        encoded = jwt.encode(
            payload,
            self.private_key,
            algorithm=self.algorithm)
        return encoded

    def decode_jwt(
            self,
            token: str | bytes,
    ) -> Optional[Dict]:
        """JWT декодирование"""
        decoded = jwt.decode(
            token,
            self.public_key,
            algorithms=[self.algorithm]
        )
        return decoded


jwt_processes = JWT()


__all__ = ['jwt_processes']