from pydantic import BaseModel


class NotificationInfo(BaseModel):
    type: str = "email"
    destination: str | None = None
    template_id: str | None = None
    template_data: dict | None = None
    content: str | None = None
