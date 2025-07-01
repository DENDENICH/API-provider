from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse

# exceptions
from pydantic import ValidationError
from exceptions.exceptions import NotFoundError, BadRequestError, ForbidenError

def error_handlers(app: FastAPI) -> None:
    """Обработчики исключений в ендпоинтах"""

    @app.exception_handler(ValidationError)
    async def pydantic_validation_error(
            request: Request,
            exc: ValidationError
    ):
        """"Обработчик ошибок валидации"""
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "message": "Unhandled validation error",
                "error": exc.errors()
            }
        )

    @app.exception_handler(NotFoundError)
    async def not_found_error(
            request: Request,
            exc: NotFoundError
    ):
        """Обработчик ошибок 404"""
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": "Not found",
                "error": str(exc)
            }
        )

    @app.exception_handler(BadRequestError)
    async def bad_request_error(
            request: Request,
            exc: BadRequestError
    ):
        """Обработчик ошибок 400"""
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "Bad request",
                "error": str(exc)
            }
        )
    @app.exception_handler(Exception)
    async def server_error(
            request: Request,
            exc: Exception
    ):
        """Обработчик ошибок 5xx"""
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Internal server error",
            }
        )