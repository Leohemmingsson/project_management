import time
import os
from uuid import uuid4

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy.orm import Session as SQLASession

from dotenv import dotenv_values

env = dotenv_values(".env")
USER = env["DB_USER"]
PASSWORD = env["DB_PASSWORD"]
HOST = env["DB_HOST"]
PORT = env["DB_PORT"]
DB_NAME = env["DB_NAME"]

mode = os.getenv("MODE", "prod")
if mode == "dev":
    HOST = "db"
    PORT = "3306"

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()


@contextmanager
def get_session():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


class SQLABaseModel(Base):
    __abstract__ = True

    @classmethod
    def add(cls, session: SQLASession, skip_id: bool = False, *args, **kwargs):
        if "id" not in kwargs and not skip_id:
            kwargs["id"] = str(uuid4())
        try:
            obj = cls(*args, **kwargs)
            session.add(obj)
            session.commit()
            return obj
        except Exception:
            session.rollback()
            raise

    @classmethod
    def add_no_commit(cls, session: SQLASession, skip_id: bool = False, *args, **kwargs):
        """
        Same function as add, but instead of commiting just flushing.

        Making it possible to add multiple times during one session with one single commit.
        """
        if "id" not in kwargs and not skip_id:
            kwargs["id"] = str(uuid4())
        obj = cls(*args, **kwargs)
        session.add(obj)
        session.flush()  # This way I can access obj.id (if not created through kwargs["id"])
        return obj

    @classmethod
    def get_all(cls, session: SQLASession):
        """
        Returns all the objects of the class
        """
        return session.query(cls).all()

    @classmethod
    def get(cls, session: SQLASession, search_query=None, sort="", start=1, length=-1):
        """
        Returns objects which can be filtered, sorted and paginated
        """
        query = session.query(cls)

        if search_query is not None:
            query = query.filter(search_query)

        total = query.count()

        if sort:
            order = []
            for s in sort.split(","):
                direction = s[0]
                name = s[1:]
                col = getattr(cls, name)
                if direction == "-":
                    col = col.desc()
                order.append(col)
            if order:
                query = query.order_by(*order)

        if start != -1 and length != -1:
            query = query.offset(start).limit(length)

        return (query.all(), total)

    @classmethod
    def get_all_where(cls, statement, session: SQLASession):
        """
        Returns all the objects of the class, where the statement is true
        """
        return session.query(cls).filter(statement).all()

    @classmethod
    def get_first_where(cls, statement, session: SQLASession):
        """
        Returns the first object of the class, where the statement is true
        """
        return session.query(cls).filter(statement).first()

    @classmethod
    def delete_where(cls, statement, session: SQLASession):
        """
        Deletes all the objects of the class, where the statement is true
        """
        session.query(cls).filter(statement).delete()
        session.commit()

    def update(self, key, value, session: SQLASession):
        """
        Updates the object with the given key and value
        """
        setattr(self, key, value)
        session.commit()

    def replace_existing_values(self, values: dict, session: SQLASession):
        """
        Replaces the existing object with the new object
        """
        for key, value in values.items():
            setattr(self, key, value)
        session.commit()

    @staticmethod
    def execute_stmt(stmt, session: SQLASession):
        """
        Executes the given statement
        """
        session.execute(stmt)
        session.commit()

    def save(self, session: SQLASession):
        """
        Same as commit
        """
        session.commit()

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"

    @property
    def as_display(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @property
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
