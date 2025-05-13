# std
from datetime import datetime, timedelta
from uuid import uuid4

# own
from ..orm import User, Token
from ..schemas import TokenPayload
from ..schemas_using_orm import RequestInfo
from ..shared_models import get_session

# pip
import jwt
from pydantic import ValidationError
from dotenv import dotenv_values
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")

env = dotenv_values(".env")
if "JWT_SECRET_KEY" not in env:
    raise Exception("JWT_SECRET_KEY not set")
JWT_SECRET_KEY = env["JWT_SECRET_KEY"]

if "JWT_ALGORITHM" not in env:
    raise Exception("JWT_ALGORITHM not set, values could be: HS256")
JWT_ALGORITHM = env["JWT_ALGORITHM"]
if "EXPIRE_IDLE_TIME_MINUTES" not in env:
    raise Exception("EXPIRE_IDLE_TIME_MINUTES not set")
EXPIRE_IDLE_TIME_MINUTES = int(env["EXPIRE_IDLE_TIME_MINUTES"])


def create_access_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode = {"user_id": str(user_id), "exp": expire, "type": "access"}

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(user_id: str, device_info, client_ip) -> str:
    expire = datetime.utcnow() + timedelta(days=7)

    to_encode = {
        "user_id": str(user_id),
        "device_info": device_info,
        "client_ip": client_ip,
        "exp": expire,
        "type": "refresh",
    }

    # Add token to DB
    with get_session() as session:
        token = Token.add(session=session, **to_encode)
        to_encode["session_id"] = token.id

    return jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)


def check_refresh_token(refresh_token: str) -> tuple:
    """
    Checking refresh_token and returns (user_id, session_id)
    """
    try:
        payload = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        token_data = TokenPayload(**payload)

        if token_data.type != "refresh":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token type")

        if token_data.user_id is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")

        with get_session() as session:
            statement = User.id == token_data.user_id
            user = User.get_first_where(statement=statement, session=session)
            if user is None:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")

        return (token_data.user_id, token_data.session_id)

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid refresh token")


def token_required(token: str = Depends(reuseable_oauth)) -> RequestInfo:
    token_data = _decode_token(token)
    request_info = _get_user_request_info(token_data)
    return request_info


def _decode_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[str(JWT_ALGORITHM)])
        token_data = TokenPayload(**payload)

    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Expired signature",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token_data


def _get_user_request_info(token_data: TokenPayload) -> RequestInfo:
    with get_session() as session:
        u_statement = User.id == token_data.user_id
        user = User.get_first_where(u_statement, session=session)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # if (datetime.now() - token.last_active) > timedelta(minutes=EXPIRE_IDLE_TIME_MINUTES):
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Token expired",
        #         headers={"WWW-Authenticate": "Bearer"},
        #     )

        request_info = RequestInfo(authorization=str(user.authorization), user=user)
    return request_info
