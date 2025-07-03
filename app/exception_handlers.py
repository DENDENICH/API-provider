from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import ORJSONResponse

# exceptions
from pydantic import ValidationError
from exceptions import BadRequestError, not_found_error
from logger import logger


def error_handlers(app: FastAPI) -> None:
    """Обработчики исключений в ендпоинтах"""

    @app.exception_handler(ValidationError)
    async def pydantic_validation_error(
            request: Request,
            exc: ValidationError
    ):
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "message": "Unprocessable entity",
                "error": exc.errors()
            }
        )

    @app.exception_handler(HTTPException)
    async def not_found_error(
            request: Request,
            exc: HTTPException
    ):
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": "Not found",
                "error": exc.detail
            }
        )

    @app.exception_handler(BadRequestError)
    async def bad_request_error(
            request: Request,
            exc: BadRequestError
    ):
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "Bad request",
                "error": str(exc)
            }
        )
    
    # Заменятся на более дружелюбные и абстрактнеы ошибки
    @app.exception_handler(Exception)
    async def other_error(
            request: Request,
            exc: Exception
    ):
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Internal server error",
            }
        )
    @app.exception_handler(not_found_error)
    async def ntf_error(
            request: Request,
            exc: not_found_error
    ):
        logger.warning('Hell')
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": "Not found custom",
            }
        )