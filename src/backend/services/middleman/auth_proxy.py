import httpx
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel

router = APIRouter(responses={404: {"description": "Not found"}})


class UserModel(BaseModel):
    """
    Class for user model.
    """

    username: str
    password: str


@router.post("/login")
def login(user: UserModel) -> Response:
    """Login endpoint for users to authenticate.

    Args:
        User (UserModel): User model, so basic user information needed to authenticate.

    Returns:
        Response: status code 200
    """
    return Response(status_code=200)


@router.post("/register")
def register(user: UserModel) -> Response:
    """Register endpoint for users to create an account.

    Args:
        user (UserModel): User model, so basic user information needed to create an account.

    Returns:
        Response: status code 200
    """
    return Response(status_code=200)
