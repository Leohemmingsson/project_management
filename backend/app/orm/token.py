from ..shared_models import SQLABaseModel
from .user import User

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session as SQLASession


class Token(SQLABaseModel):
    __tablename__ = "token"
    id = Column(String(255), primary_key=True, nullable=False)
    authorization = Column(String(30), nullable=False)
    device_info = Column(String(255), nullable=False)
    client_ip = Column(String(45))
    exp = Column(DateTime)
    type = Column(String(50))
    is_active = Column(Boolean, default=True, nullable=False)
    last_active = Column(DateTime)

    # Foreign key to User
    user_id = Column(String(255), ForeignKey("user.id"), nullable=True)

    # Relationship to User
    user = relationship("User", back_populates="tokens")

    @classmethod
    def add(cls, session: SQLASession, *args, **kwargs):
        """
        Overwrites the default add method

        Creates id and authorization if not already set.
        Also checking that user exists
        """
        if "authorization" not in kwargs:
            user = kwargs.get("user", None)
            user_id = kwargs.get("user_id", None)

            if user:
                kwargs["authorization"] = user.authorization
            elif user_id:
                statement = User.id == user_id
                user_obj = User.get_first_where(session=session, statement=statement)
                if user_obj is None:
                    raise Exception(f"User does not exist, when creating token with user_id: {user_id}")
                kwargs["authorization"] = user_obj.authorization

            else:
                kwargs["authorization"] = "R"

        return super().add(session=session, *args, **kwargs)
