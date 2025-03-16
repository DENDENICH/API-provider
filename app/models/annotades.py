from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column

from typing import Annotated


intpk = Annotated[
    int,
    mapped_column(Integer, primary_key=True) 
    ]