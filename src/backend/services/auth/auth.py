"""
This file contains the auth routes for the FastAPI application.
"""

# Imports
from exceptions import CREDENTIALS_EXECPTION

from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel

from wrapper import Wrapper

router = APIRouter(responses={404: {"description": "Not found"}})


class UserModel(BaseModel):
    """
    Class for user model.
    """

    username: str
    password: str


# Routes
@router.post("/login")
async def login_for_access_token(user: UserModel) -> Response:
    """Login endpoint for users to authenticate.

    Args:
        User (UserModel): User model, so basic user information needed to authenticate.

    Returns:
        Response: status code 200
    """
    auth_wrapper = Wrapper()

    if not user.username or not user.password:
        raise CREDENTIALS_EXECPTION

    if not auth_wrapper.check_user_exists(user.username):
        raise CREDENTIALS_EXECPTION

    if user.password != auth_wrapper.get_password(user.username):
        raise CREDENTIALS_EXECPTION

    auth_wrapper.close()
    return Response(status_code=200)



@router.post("/register")
async def register(user: UserModel) -> Response:
    """Register endpoint for users to create an account.

    Args:
        user (UserModel): User model, so basic user information needed to create an account.

    Returns:
        Response: status code 200
    """
    auth_wrapper = Wrapper()

    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Username or password not provided")

    if auth_wrapper.check_user_exists(user.username):
        raise HTTPException(status_code=400, detail="User already exists")
    
    auth_wrapper.create_user(user.username, user.password)

    auth_wrapper.close()
    return Response(status_code=200)
