from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse

# exceptions
from pydantic import ValidationError
from exceptions.exceptions import NotFoundError, BadRequestError, ForbidenError

from exceptions.utils import ROLLBACK_SESSION_METHODS


def user_error_handlers(app: FastAPI) -> None:
    """Обработчики пользовательских исключений в ендпоинтах"""

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
    
    @app.exception_handler(BadRequestError)
    async def bad_request_error(
            request: Request,
            exc: BadRequestError
    ):
        """Обработчик ошибок 400"""
        await request.state.session.rollback() if request.method in ROLLBACK_SESSION_METHODS else None

        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "Bad request",
                "error": str(exc)
            }
        )
    
    @app.exception_handler(ForbidenError)
    async def forbiden_error(
            request: Request,
            exc: BadRequestError
    ):
        """Обработчик ошибок 403"""

        return ORJSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "message": "Access is denied",
                "error": str(exc)
            }
        )

    @app.exception_handler(NotFoundError)
    async def not_found_error(
            request: Request,
            exc: NotFoundError
    ):
        """Обработчик ошибок 404"""
        await request.state.session.rollback() if request.method in ROLLBACK_SESSION_METHODS else None

        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": "Resource not found",
                "error": str(exc)
            }
        )
    