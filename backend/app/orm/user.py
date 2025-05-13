from ..utils import hash_password

from ..shared_models import SQLABaseModel
from ..connections import send_email, send_sms
from ..schemas import NotificationInfo

from sqlalchemy import Column, String, DateTime  # , Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session as SQLASession

from fastapi import HTTPException, status


class User(SQLABaseModel):
    __tablename__ = "user"
    id = Column(String(255), primary_key=True, nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(30))
    hashed_password = Column(String(255), nullable=False)
    authorization = Column(String(30), nullable=False)
    last_active = Column(DateTime)

    tokens = relationship("Token", back_populates="user")

    def __repr__(self):
        return (
            f"<User {self.id}, name: {self.name}, authorization: {self.authorization}>"
        )

    def send_notification(self, notification_info: NotificationInfo):
        if notification_info.type == "email":
            notification_info.destination = self.email
            send_email(notification_info)
        elif notification_info.type == "sms":
            notification_info.destination = self.phone
            send_sms(notification_info)
        else:
            raise ValueError(
                f"Unexpected type when sending notifiction: {notification_info.type}"
            )

    @classmethod
    def add(cls, session: SQLASession, *args, **kwargs):
        """
        Overwrites the default add method

        Creates id and authorization if not already set.
        Also hashes passwords
        """
        statement = cls.name == kwargs["name"]
        if cls.get_first_where(session=session, statement=statement):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Name already exists"
            )

        if "authorization" not in kwargs:
            kwargs["authorization"] = "RW"

        if "password" in kwargs:
            kwargs["hashed_password"] = hash_password(kwargs["password"])
            del kwargs["password"]

        return super().add(session=session, *args, **kwargs)

    @property
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "authorization": self.authorization,
        }

    @property
    def as_display(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "authorization": self.authorization,
        }
