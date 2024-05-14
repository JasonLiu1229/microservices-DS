# Imports
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from wrapper import Wrapper

router = APIRouter(responses={404: {"description": "Not found"}})


class Calendar(BaseModel):
    """Calendar model."""

    user_id: int
    shared_with_id: int


class CalendarReturn(BaseModel):
    """Calendar model."""

    user_id: int
    shared_with_id: int
    calendar_id: int


@router.get("")
def get_calendars(user_id: int) -> list[dict]:
    """
    Get all shared calendars.
    """
    try:
        wrapper = Wrapper()
        calendars = wrapper.get_shared_calendars(user_id)
        return [
            {
                "user_id": getattr(calendar, "user_id"),
                "shared_with_id": getattr(calendar, "shared_with_id"),
                "calendar_id": getattr(calendar, "id"),
            }
            for calendar in calendars
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("")
def create_share(calendar: Calendar) -> CalendarReturn:
    """
    Share calendar.
    """
    try:
        wrapper = Wrapper()
        calendar_return = wrapper.create_share(
            user_id=calendar.user_id, share_id=calendar.shared_with_id
        )
        return {
            "user_id": getattr(calendar_return, "user_id"),
            "shared_with_id": getattr(calendar_return, "shared_with_id"),
            "calendar_id": getattr(calendar_return, "id"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
