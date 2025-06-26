from fastapi import HTTPException, status


forbiden_error = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, 
    detail="Forbiden error"
)


not_found_error = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, 
    detail="Not found"
)


class NotFoundError(Exception):
    """Ошибка - не найдено"""
    pass


class BadRequestError(Exception):
    """Ошибка ошибочного или/и плохого запроса"""
    pass