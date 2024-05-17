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
    response = httpx.post(
        "http://backend-auth:8000/auth/login",
        json={"username": user.username, "password": user.password},
    )
    if response.status_code == 200:
        return Response(status_code=200)
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@router.post("/register")
def register(user: UserModel) -> Response:
    """Register endpoint for users to create an account.

    Args:
        user (UserModel): User model, so basic user information needed to create an account.

    Returns:
        Response: status code 200
    """
    response = httpx.post(
        "http://backend-auth:8000/auth/register",
        json={"username": user.username, "password": user.password},
    )
    if response.status_code == 200:
        return Response(status_code=200)
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
