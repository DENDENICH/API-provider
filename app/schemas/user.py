from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):

    # По умолчанию уже есть, используется для совместимости с объектом БД
    # model_config = ConfigDict(
    #     from_attributes=True
    # )

    id: int 
