from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse

# exceptions
from pydantic import ValidationError
from exceptions import NotFoundError, BadRequestError

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
                "message": "Unhandled validation error",
                "error": exc.errors()
            }
        )

    @app.exception_handler(NotFoundError)
    async def not_found_error(
            request: Request,
            exc: NotFoundError
    ):
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
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "Bad request",
                "error": str(exc)
            }
        )
    
    # Заменятся на более дружелюбные и абстрактнеы ошибки
    @app.exception_handler(BadRequestError)
    async def bad_request_error(
            request: Request,
            exc: Exception
    ):
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Internal server error",
            }
        )