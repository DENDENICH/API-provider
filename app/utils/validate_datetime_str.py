from functools import singledispatchmethod
from datetime import datetime

class ValidateYearMonthDate:
    """Валидация строки даты в формате 'YYYY-MM'"""

    @singledispatchmethod
    @staticmethod
    def validate(date):
        raise TypeError("Incorrect data type")

    @validate.register(str)    
    @staticmethod
    def _validate_from_str(date: str) -> str:
        """Проверяет, что строка даты в формате 'YYYY-MM' и возвращает объект datetime.

        Args:
            date_str (str): Строка даты в формате 'YYYY-MM'.

        Returns:
            str: Объект str, соответствующий формату

        Raises:
            ValueError: Если строка даты не соответствует формату 'YYYY-MM'.
        """
        try:
            validate_date = datetime.strptime(date, "%Y-%m")
            del validate_date
            return date
        except ValueError as e:
            raise ValueError(f"Неверный формат даты: {date}. Ожидается 'YYYY-MM'.")
        
    @validate.register(datetime)
    @staticmethod
    def _validate_from_datetime(date: datetime) -> str:
        """
        Args:
            date_str (datetime).

        Returns:
            str: Объект str, соответствующий формату 'YYYY-MM'.

        Raises:
            ValueError: Если не удалось распарсить объект в строку в формате 'YYYY-MM'.
        """
        try:
            return date.strftime("%Y-%m")
        except ValueError as e:
            raise ValueError(f"Не удалось распарсить объект: {date} в строку 'YYYY-MM'.")
        