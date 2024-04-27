"""
This file contains the security routes for the FastAPI application.
"""

# Imports
import datetime
import json

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from wrapper import add_token, del_token, create_user, find_user

from dependencies import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    check_token_validity,
    create_access_token,
    get_password_hash,
)

router = APIRouter(responses={404: {"description": "Not found"}})

class UserModel(BaseModel):
    """
    Class for user model.
    """

    username: str
    password: str


# helper functions
def create_user_token(username: str, password: str) -> str:
    """Create user token.

    Args:
        username (str): username of user
        password (str): password of user

    Returns:
        str: token
    """
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": username, "password": password},
        expires_delta=access_token_expires,
    )
    return str(access_token)


# Routes
@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Response:
    """Login endpoint for users to authenticate and receive an access token.

    Args:
        form_data (OAuth2PasswordRequestForm, optional): OAuth2 form. Defaults to Depends().

    Returns:
        Response: Access token
    """
    # authenticate user
    if not (user := authenticate_user(form_data.username, form_data.password)):
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="Incorrect username or password",
        )
    # create access token
    access_token = create_user_token(form_data.username, form_data.password)

    try:
        user = find_user(form_data.username)
        # add user token to database
        add_token(access_token, int(user.id))
    except ValueError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content="User not found",
        )

    # return access token
    return Response(
        status_code=status.HTTP_200_OK,
        content="Login successful",
        headers={"Authorization": f"Bearer {access_token}"},
    )


@router.post("/register")
async def register(user: UserModel) -> Response:
    """Register endpoint for users to create an account and receive an access token.

    Args:
        user (UserModel): User model, so basic user information needed to create an account.

    Returns:
        Response: Access token
    """

    # create user
    try:
        hashed_password = get_password_hash(user.password)
        user_instance = create_user(user.username, hashed_password)
    except ValueError:
        return Response(
            status_code=status.HTTP_409_CONFLICT, content="Username already registered"
        )

    # create access token
    access_token = create_user_token(user.username, user.password)

    # add user token to database
    try:
        add_token(access_token, int(user_instance.id))
    except ValueError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content="User not found",
        )

    # return username and access token
    return Response(
        status_code=status.HTTP_200_OK,
        content=json.dumps({"username": user.username}),
        headers={"Authorization": f"Bearer {access_token}"},
    )


@router.put("/logout")
async def logout(request: Request) -> Response:
    """Logout endpoint for users to log out and invalidate their access token.

    Args:
        request (Request): Request object, contains the Authorization header with the token.

    Returns:
        Response: Success message or error message
    """
    # get the token from the Authorization header
    cookie = request.headers.get("Authorization", None)
    if not (cookie or isinstance(cookie, str)):
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="Not Authorized",
        )

    if not cookie.startswith("Bearer "):
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="Not Authorized",
        )

    token = cookie.split(" ")[1]
    try:
        del_token(token)
    except ValueError:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content="Token not found",
        )

    return Response(
        status_code=status.HTTP_200_OK,
        content=json.dumps({"message": "User logged out"}),
    )


@router.get("/status")
async def get_status(request: Request) -> Response:
    """Get the status of the user session.

    Args:
        request (Request): Request object, contains the Authorization header with the token.

    Returns:
        Response: Success message or error message
    """
    # get cookie from request headers
    cookie = request.headers.get("Authorization", None)
    if not (cookie or isinstance(cookie, str)):
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="No cookie provided in headers",
        )

    if not cookie.startswith("Bearer "):
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="Invalid cookie format",
        )

    token = cookie.split(" ")[1]

    # unpack cookie
    try:
        await check_token_validity(token)
    except HTTPException as exc:
        return Response(
            status_code=exc.status_code,
            content=exc.detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Response(
        status_code=status.HTTP_200_OK,
        content="User session is active",
    )
