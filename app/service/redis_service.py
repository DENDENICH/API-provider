import redis.asyncio as aioredis
import json
from typing import Optional, TypedDict
from logger import logger


class UserContext(TypedDict):
    user_company_id: Optional[int]
    user_company_role: Optional[str]
    organizer_id: Optional[int]
    organizer_role: Optional[str]


class RedisStorage:
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

    async def set_user_data(
            self, 
            user_id: int, 
            user_context: UserContext, 
            expire: int = 86_400
    ) -> None:
        """Установка значений пользователя"""
        await self.redis.set(str(user_id), json.dumps(user_context), ex=expire)
        logger.info(
            msg=f"Set data user from redis\nid - {user_id}\ncontext - {user_context}"
        )

    async def get_user_data(self, user_id: int) -> Optional[UserContext]:
        """Получение пользователя по id"""
        user_context = await self.redis.get(str(user_id))
        if user_context:
            logger.info(
                msg=f"Get data user from redis\nid - {user_id}\ncontext - {user_context}"
            )
            return UserContext(**json.loads(user_context))
        return None

    async def delete_user_data(self, user_id: int) -> None:
        """Удаление пользователя по id"""
        await self.redis.delete(str(user_id))



redis = RedisStorage()
