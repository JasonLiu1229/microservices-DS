# Imports
from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel

from wrapper import Wrapper

router = APIRouter(responses={404: {"description": "Not found"}})


class Calendar(BaseModel):
    """Calendar model."""

    user_id: int
    shared_with_id: int


@router.get("")
def get_calendars(user_id: int) -> list[dict]:
    """
    Get all shared calendars.
    """
    try:
        wrapper = Wrapper()
        calendars = wrapper.get_shared_calendars(user_id)
        return Response(status_code=200, content=calendars)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("")
def create_share(calendar: Calendar) -> None:
    """
    Share calendar.
    """
    try:
        wrapper = Wrapper()
        wrapper.create_share(user_id=calendar.user_id, share_id=calendar.shared_with_id)
        return Response(status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
