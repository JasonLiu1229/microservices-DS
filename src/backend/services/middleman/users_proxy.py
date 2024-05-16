import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

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
    response = httpx.get("http://backend-auth:8000/users")
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@router.get("/{user_id}")
async def get_user(user_id: int) -> UserReturn:
    """Get user.

    Args:
        user_id (int): user id

    Returns:
        Response: 200 OK
    """
    response = httpx.get(f"http://backend-auth:8000/users/{user_id}")
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
