# own
from ..orm import User
from ..schemas_using_orm import RequestInfo

# pip
from fastapi import HTTPException


def check_authorized(
    request_info: RequestInfo | None = None,
    required_permission: str = "A",
    user: User | None = None,
    exception_user_id: str | None = None,
):
    """
    Checks if user is authorized to perform an action
    user: This is the user trying to access something/perform an action
    required_permission: This is the permission required to perform the action
        ex)"S" for super user, "A" for admin, "R" for read, "W" for write
        These can be combined ex) "RW" or "WR" for read and write

    exception_user_id: This is the user id of the user that can perform the action no matter the authorization of user

    Permissions:
        S > A > (R and W)
        If using other permissions it will be at the same level as (R and W)
    """
    if request_info is None:
        if user is None:
            raise HTTPException(status_code=401, detail="Not authorized")
        authorization = str(user.authorization)
    else:
        authorization = str(request_info.authorization)
        if request_info.user is not None:
            user = request_info.user

    if "S" in authorization:
        return True

    if "A" in authorization and required_permission != "S":
        return True

    if (user is not None) and (exception_user_id is not None):
        if str(user.id) == exception_user_id:
            return True

    for permission in required_permission:
        if permission not in authorization:
            raise HTTPException(status_code=403, detail="Not authorized")

    return True
