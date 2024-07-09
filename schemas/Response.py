from pydantic import BaseModel


class Response(BaseModel):
    code: int
    data: str
    msg: str


class OKResponse(Response):
    def __init__(self, code=200, data="", msg="success"):
        super().__init__(code=code, data=data, msg=msg)


class ErrorResponse(Response):
    def __init__(self, code=400, data="", msg="error"):
        super().__init__(code=code, data=data, msg=msg)
