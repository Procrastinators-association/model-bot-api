from pydantic import BaseModel


class ResultOk(BaseModel):
    result: str = "Ok"


class ResultError(BaseModel):
    result: str = "Something went wrong, contact the site crew"
