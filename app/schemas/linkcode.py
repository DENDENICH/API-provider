from pydantic import BaseModel

class LinkCodeResponse(BaseModel):
    linkcode: int
