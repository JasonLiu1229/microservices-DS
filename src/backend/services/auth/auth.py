"""
This file contains the auth routes for the FastAPI application.
"""

# Imports
from exceptions import CREDENTIALS_EXECPTION, NOT_FOUND_EXCEPTION

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
def login(user: UserModel) -> Response:
    """Login endpoint for users to authenticate.

    Args:
        User (UserModel): User model, so basic user information needed to authenticate.
        
    HttpExceptions:
        401: Unauthorized
        404: Not found
        400: Bad request

    Returns:
        Response: status code 200
    """
    auth_wrapper = Wrapper()

    if not user.username or not user.password:
        raise CREDENTIALS_EXECPTION

    if not auth_wrapper.check_user_exists(user.username):
        raise NOT_FOUND_EXCEPTION

    if user.password != auth_wrapper.get_password(user.username):
        raise CREDENTIALS_EXECPTION

    auth_wrapper.close()
    return Response(status_code=200)



@router.post("/register")
def register(user: UserModel) -> Response:
    """Register endpoint for users to create an account.

    Args:
        user (UserModel): User model, so basic user information needed to create an account.
    
    HttpExceptions:
        400: Bad request

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
