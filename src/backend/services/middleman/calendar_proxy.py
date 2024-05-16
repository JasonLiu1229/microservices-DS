import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

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
def get_calendars() -> list[CalendarReturn]:
    """
    Get all shared calendars.
    """
    response = httpx.get("http://backend-calendar:8000/calendars/")
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@router.get("/{calendar_id}")
def get_calendar(calendar_id: int) -> CalendarReturn:
    """
    Get shared calendar.
    """
    response = httpx.get(f"http://backend-calendar:8000/calendars/{calendar_id}")
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@router.post("")
def create_share(calendar: Calendar) -> CalendarReturn:
    """
    Share calendar.
    """
    # Additonal validation of user_id and shared_with_id
    if calendar.user_id == calendar.shared_with_id:
        raise HTTPException(status_code=400, detail="User cannot share calendar with themselves.")
    
    # check if users exist
    response = httpx.get(f"http://backend-auth:8000/users/{calendar.user_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    response = httpx.get(f"http://backend-auth:8000/users/{calendar.shared_with_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    response = httpx.post("http://backend-calendar:8000/calendars/", json={
        "user_id": calendar.user_id,
        "shared_with_id": calendar.shared_with_id
    })
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
