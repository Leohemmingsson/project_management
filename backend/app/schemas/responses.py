# pip
from pydantic import BaseModel


class ListResponse(BaseModel):
    data: list
    total: int
