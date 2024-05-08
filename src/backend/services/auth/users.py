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
