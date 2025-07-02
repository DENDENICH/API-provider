from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse

# exceptions
from sqlalchemy.exc import DatabaseError
from redis.exceptions import RedisError

from exceptions.utils import ROLLBACK_SESSION_METHODS

from logger import logger


def server_error_handlers(app: FastAPI) -> None:
    """Обработчики пользовательских исключений в ендпоинтах"""

    @app.exception_handler(DatabaseError)
    async def database_error(
            request: Request,
            exc: DatabaseError
    ):
        """"Обработчик ошибок базы данных"""
        await request.state.session.rollback() if request.method in ROLLBACK_SESSION_METHODS else None

        logger.critical(
            msg="Internal database error",
            exc_info=exc
        )

        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Internal database error",
                "error": exc.detail
            }
        )
    
    @app.exception_handler(RedisError)
    async def redis_error(
            request: Request,
            exc: RedisError
    ):
        """Обработчик ошибок redis"""
        await request.state.session.rollback() if request.method in ROLLBACK_SESSION_METHODS else None

        logger.critical(
            msg="Redis service error",
            exc_info=exc
        )
        
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Internal database error",
                "error": str(exc)
            }
        )
    