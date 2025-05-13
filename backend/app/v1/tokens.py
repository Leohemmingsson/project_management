# own
from ..shared_models import get_session
from ..permissions import token_required, check_authorized
from ..schemas import ListResponse
from ..schemas_using_orm import RequestInfo
from ..orm import Token
from ..custom_responses import make_list_response

# pip
from fastapi import APIRouter, Depends
from sqlalchemy import or_, and_


router = APIRouter(
    prefix="/token",
    tags=["Token"],
)


@router.get("/", status_code=200)
def get_tokens(
    request_info: RequestInfo = Depends(token_required),
    search: str = "",
    sort: str = "",
    start: int = 0,
    length: int = 10,
) -> ListResponse:
    """
    Returns all users

    *Authorization*: Admin
    """

    check_authorized(request_info, "R")

    with get_session() as session:
        statement = and_(
            or_(Token.id.like(f"%{search}%"), Token.user_id.like(f"%{search}%")), Token.user_id == request_info.user.id
        )
        tokens, total = Token.get(search_query=statement, sort=sort, start=start, length=length, session=session)
        tokens = [token.as_display for token in tokens]
    return make_list_response(tokens, total=total)


@router.delete("/", status_code=204)
def delete_token(token_id: str, request_info: RequestInfo = Depends(token_required)):
    """ """
    check_authorized(request_info, "W")

    with get_session() as session:
        statement = Token.id == token_id
        token = Token.get_first_where(session=session, statement=statement)
        if token.user_id == request_info.user.id:
            Token.delete_where(session=session, statement=statement)
        else:
            check_authorized(request_info, "A")
            Token.delete_where(session=session, statement=statement)
