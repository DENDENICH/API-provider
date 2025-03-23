from pydantic import BaseModel


class AuthResponse(BaseModel):
    access_token: str
    type_token: str
