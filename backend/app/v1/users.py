# own
from ..shared_models import get_session
from ..permissions import token_required, check_authorized
from ..schemas import ListResponse, UserSchema, UserPermission
from ..schemas_using_orm import RequestInfo
from ..orm import User
from ..custom_responses import make_list_response

# pip
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/", status_code=200)
def get_users(
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
        statement = or_(User.name.like(f"%{search}%"), User.email.like(f"%{search}%"))
        users, total = User.get(search_query=statement, sort=sort, start=start, length=length, session=session)
        users = [user.as_display for user in users]
    return make_list_response(users, total=total)


@router.post("/", status_code=200)
def add_user(user_info: UserSchema, request_info: RequestInfo = Depends(token_required)) -> dict:
    """
    Returns all users

    *Authorization*: Admin
    """

    check_authorized(request_info, "A")

    with get_session() as session:
        added_user = User.add(session=session, **user_info.dict())
        display_user = added_user.as_display
    return {"created_user": display_user}


@router.post("/update_permission", status_code=204)
def change_permissions(user_info: UserPermission, request_info: RequestInfo = Depends(token_required)):
    """
    Changing permissions for existing users.

    If new permission is below admin, a admin can set it.
    If the permission is admin, only a super user can set it.
    It is not allowed to add a new super user.

    TODO:
        - Might need to update so there is priviledged admin to create new admins

    *Authorization*: Admin/Super user
    """

    if "S" in user_info.new_permission:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    elif "A" in user_info.new_permission:
        check_authorized(request_info, "S")
    else:
        check_authorized(request_info, "A")

    with get_session() as session:
        statement = User.id == user_info.id
        user_to_modify = User.get_first_where(session=session, statement=statement)
        user_to_modify.update(session=session, key="authorization", value=user_info.new_permission)
