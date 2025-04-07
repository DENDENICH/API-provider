from bcrypt import hashpw, gensalt, checkpw


class HashPassword:
    """Класс для хэширования пользовательского пароля, 
    а также его проверка на совпадение с хэшем"""
    def create_hash(
            self,
            password: str
    ) -> bytes:
        return hashpw(password.encode(), gensalt())

    def check_password(
            self,
            password: str,
            hash: bytes
    ) -> bool:
        return checkpw(password.encode(), hash) # True если совпадает


hashing_password = HashPassword()


__all__ = ['hashing_password']
