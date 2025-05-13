from typing import TYPE_CHECKING, Union
from pydantic import BaseModel
from ..orm import User

class RequestInfo(BaseModel):
    authorization: str
    user: User | None = None

    class Config:
        arbitrary_types_allowed = True
