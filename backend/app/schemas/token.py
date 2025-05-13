from pydantic import BaseModel
from datetime import datetime


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    user_id: str | None = None
    session_id: str | None = None
    exp: datetime | None = None
    type: str | None = None


class TokenCreateSchema(BaseModel):
    name: str
    authorization: str
    is_active: bool = True
