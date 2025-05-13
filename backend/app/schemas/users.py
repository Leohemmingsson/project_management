from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    email: str
    phone: str | None = None
    password: str


class UserPermission(BaseModel):
    id: str
    new_permission: str
