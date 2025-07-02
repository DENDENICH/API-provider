from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse

# exceptions
from sqlalchemy.exc import DataError, IntegrityError, OperationalError, SQLAlchemyError
from redis.exceptions import RedisError

from exceptions.utils import ROLLBACK_SESSION_METHODS

from logger import logger


def server_error_handlers(app: FastAPI) -> None:
    """Обработчики пользовательских исключений в ендпоинтах"""

    @app.exception_handler(SQLAlchemyError)
    async def database_error(
            request: Request,
            exc: SQLAlchemyError
    ):
        """"Обработчик ошибок базы данных"""
        await request.state.session.rollback() if request.method in ROLLBACK_SESSION_METHODS else None

        logger.critical(
            msg="Internal database error",
            exc_info=exc
        )

        if isinstance(exc, IntegrityError):
            status_code = status.HTTP_409_CONFLICT
            detail = "Data conflict integrity"
        elif isinstance(exc, OperationalError):
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            detail = "Database unavailable"
        elif isinstance(exc, DataError):
            status_code = status.HTTP_400_BAD_REQUEST
            detail = "Invalid data format"
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "An unintended error"

        return ORJSONResponse(
            status_code=status_code,
            content={
                "message": "Internal database error",
                "error": detail
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

    @app.exception_handler(Exception)
    async def unhandled_exception(
            request: Request,
            exc: Exception
    ):
        """Обработчик необработанных (неизвестных) исключений"""
        await request.state.session.rollback() if request.method in ROLLBACK_SESSION_METHODS else None

        logger.critical(
            msg="Internal unhandled server error",
            exc_info=exc
        )

        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Internal server error",
                "error": str(exc)
            }
        )
    