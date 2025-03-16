from dataclasses import dataclass
from datetime import timedelta, datetime

import jwt

# временные данные
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


@dataclass(frozen=True)
class JWT:
    """Class for encode and decode JWT properties"""
    private_key: str = SECRET_KEY
    #public_key: str = settings.auth.public_key.read_text()
    algorithm: str = ALGORITHM
    access_token_expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES

    def encode_jwt(
            self,
            payload: dict,
            expire_timedelta: timedelta | None = None
    ):
        """JWT encode function:
        payload -> object for encode
        expire_timedelta -> shows how long it will take for the token to expire"""

        to_encode = payload.copy()
        now = datetime.now()

        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(
                minutes=self.access_token_expire_minutes
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
    ):
        """JWT encode function"""
        try:
            decoded = jwt.decode(
                token,
                self.private_key,
                algorithms=[self.algorithm])
            return decoded
        except jwt.ExpiredSignatureError:
            raise ValueError('Token expired')
        except jwt.InvalidTokenError:
            raise ValueError('Invalid token')

jwt_processes = JWT()


__all__ = ['jwt_processes']