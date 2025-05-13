# std
from datetime import datetime

# Own
from ..orm import User, Token
from ..schemas import TokenSchema
from ..permissions import create_access_token, create_refresh_token, check_refresh_token
from ..utils import is_password_correct
from ..shared_models import get_session

# pip
from fastapi import APIRouter, status, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from user_agents import parse

router = APIRouter(
    prefix="",
    tags=["Authorization"],
)


@router.post("/login", summary="Create access token for user", response_model=TokenSchema)
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    request_info = parse_request_info(request)
    with get_session() as session:
        statement = User.name == form_data.username
        user = User.get_first_where(statement, session=session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

        if not is_password_correct(form_data.password, str(user.hashed_password)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

        user.last_active = datetime.now()
        user.save(session)

        return {
            "access_token": create_access_token(user_id=user.id),
            "refresh_token": create_refresh_token(user_id=user.id, **request_info),
        }


@router.post("/refresh", summary="Refresh access token", response_model=TokenSchema)
def refresh_token(request: Request, refresh_token: str):
    user_id, session_id = check_refresh_token(refresh_token=refresh_token)
    request_info = parse_request_info(request)

    # Remove current token
    with get_session() as session:
        statement = Token.id == session_id
        Token.delete_where(session=session, statement=statement)

    return {
        "access_token": create_access_token(user_id=user_id),
        "refresh_token": create_refresh_token(user_id=user_id, **request_info),
    }


def parse_request_info(request: Request) -> dict:
    """
    Returns dict with keys
    * device_info
    * client_ip
    """
    return_value = {}
    user_agent = request.headers.get("user-agent")

    user_agent = parse(user_agent)
    return_value["device_info"] = f"{user_agent.browser.family} on {user_agent.os.family}"
    return_value["client_ip"] = _get_client_ip(request)
    return return_value


def _get_client_ip(request: Request):
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        ip_list = [ip.strip() for ip in x_forwarded_for.split(",") if ip.strip()]
        if ip_list:
            return ip_list[0]
    return request.client.host
