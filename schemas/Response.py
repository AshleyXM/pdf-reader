from pydantic import BaseModel


class Response(BaseModel):
    code: int
    data: str
    msg: str
