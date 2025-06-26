from abc import ABC, abstractmethod
from typing import Optional, Any

import redis.asyncio as aioredis
import json

from logger import logger


class UserDataRedis:
    def __init__(
            self,
            user_id: int = None,
            user_company_id: int = None,
            user_company_role: str = None,
            organizer_id: int = None,
            organizer_role: str = None
        ):
        self.user_id = user_id
        self.user_company_id = user_company_id
        self.user_company_role = user_company_role
        self.organizer_id = organizer_id
        self.organizer_role = organizer_role 
        
    @property
    def to_dict(self):
        return self.__dict__


class RedisBase(ABC):
    __instance: dict = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls.__instance:
            cls.__instance[cls] = super().__new__(cls)
        return cls.__instance[cls]

    def __init__(self, host: str = "localhost", port: int = 6379):
        self.redis = aioredis.Redis(
            host=host,
            port=port
        )

    @abstractmethod
    async def set_data(
            self, 
            key: Any, 
            data: Any,
            expire_seconds: int
    ) -> None:
        pass

    @abstractmethod
    async def get_data(self, key: Any) -> Optional[dict]:
        pass

    @abstractmethod
    async def delete_data(self, key: Any) -> None:
        pass


class RedisUser(RedisBase):
    """Класс для работы с данными пользователя в хранилище Redis"""

    async def set_data(
            self, 
            key: int, 
            data: UserDataRedis, 
            expire_seconds: int = 86_400
    ) -> None:
        await self.redis.set(str(key), json.dumps(data.to_dict), ex=expire_seconds)
        logger.info(
            msg=f"Set data user from redis\nid - {key}\ncontext - {data}"
        )

    async def get_data(self, key: int) -> Optional[UserDataRedis]:
        data = await self.redis.get(str(key))
        if data:
            logger.info(
                msg=f"Get data user from redis\nid - {key}\ncontext - {data}"
            )
            return UserDataRedis(**json.loads(data))
        return None

    async def delete_data(self, key: int) -> None:
        await self.redis.delete(str(key))


redis_user = RedisUser()
