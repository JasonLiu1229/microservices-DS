from fastapi import APIRouter, Response
from wrapper import Wrapper

router = APIRouter(responses={404: {"description": "Not found"}})

@router.get("")
async def get_users() -> Response:
    """Get all users.

    Returns:
        Response: 200 OK
    """
    auth_wrapper = Wrapper()
    users = auth_wrapper.get_users()
    users_username = [user.username for user in users]
    return Response(content={"users": users_username}, status_code=200)

@router.get("/{user_id}")
async def get_user(user_id: int) -> Response:
    """Get user.

    Args:
        user_id (int): user id

    Returns:
        Response: 200 OK
    """
    try:
        auth_wrapper = Wrapper()
        user = auth_wrapper.get_user(user_id)
        return Response(content=user, status_code=200)
    except ValueError as e:
        return Response(content=str(e), status_code=404)
