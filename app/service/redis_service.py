from abc import ABC, abstractmethod
from typing import Optional, Any
from dataclasses import dataclass

import redis.asyncio as aioredis
import json

from logger import logger

@dataclass()
class UserDataRedis:
    user_id: Optional[int]
    user_company_id: Optional[int]
    user_company_role: Optional[str]
    organizer_id: Optional[int]
    organizer_role: Optional[str]


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
        await self.redis.set(str(key), json.dumps(data), ex=expire_seconds)
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

    # async def get_organizer_id_by_user_id(self, user_id: int) -> int:
    #     user = await self.get_data(user_id)
    #     return user.organizer_id
    
    # async def get_organizer_role_by_user_id(self, user_id: int) -> str:
    #     user = await self.get_data(user_id)
    #     return user["organizer_role"]
    
    # async def get_user_company_id_by_user_id(self, user_id: int) -> int:
    #     user = await self.get_data(user_id)
    #     return user["user_company_id"]

    # async def get_user_company_role_by_user_id(self, user_id: int) -> str:
    #     user = await self.get_data(user_id)
    #     return user["user_company_role"]
    


redis_user = RedisUser()
