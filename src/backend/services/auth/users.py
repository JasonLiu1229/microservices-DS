from fastapi import APIRouter, Response, HTTPException
import sqlalchemy.exc as db_exc

from pydantic import BaseModel
from wrapper import Wrapper

router = APIRouter(responses={404: {"description": "Not found"}})


class UserReturn(BaseModel):
    """User model."""

    username: str
    user_id: int


@router.get("")
async def get_users() -> list[UserReturn]:
    """Get all users.

    Returns:
        Response: 200 OK
    """
    try:
        auth_wrapper = Wrapper()
        users = auth_wrapper.get_users()
        return [
            {"username": getattr(user, "username"), "user_id": getattr(user, "id")} for user in users
        ]
    except db_exc.NoResultFound as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    

@router.get("/{user_id}")
async def get_user(user_id: int) -> UserReturn:
    """Get user.

    Args:
        user_id (int): user id

    Returns:
        Response: 200 OK
    """
    try:
        auth_wrapper = Wrapper()
        user = auth_wrapper.get_user(user_id)
        return {"username": getattr(user, "username"), "user_id": getattr(user, "id")}
    except ValueError as e:
        return Response(content=str(e), status_code=404)
