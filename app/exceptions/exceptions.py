

class NotFoundError(Exception):
    """Ошибка - не найдено"""
    pass


class BadRequestError(Exception):
    """Ошибка ошибочного или/и плохого запроса"""
    pass


class ForbidenError(Exception):
    """Ошибка запрещенного действия"""
    pass
