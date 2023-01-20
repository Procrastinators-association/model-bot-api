from pydantic import BaseModel


class ProcessFiles(BaseModel):
    accepted: list
    not_accepted: list
