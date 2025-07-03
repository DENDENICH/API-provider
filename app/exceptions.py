from fastapi import HTTPException, status


forbiden_error = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, 
    detail="Forbiden error"
)

not_found_error = None


# not_found_error = HTTPException(
#     status_code=status.HTTP_404_NOT_FOUND, 
#     detail="Not found"
# )

from fastapi import HTTPException, status

class SomeError(HTTPException):
    def __init__(self, detail: str = "Not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)



class NotFoundError(Exception):
    """Ошибка - не найдено"""
    pass


class BadRequestError(Exception):
    """Ошибка ошибочного или/и плохого запроса"""
    pass