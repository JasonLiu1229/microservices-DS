from datetime import datetime

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(responses={404: {"description": "Not found"}})


class Event(BaseModel):
    """Event model."""

    organizer_id: int
    title: str
    description: str
    date: datetime = Field(..., description="Date in YYYY-MM-DD format")
    is_public: bool


class EventReturn(BaseModel):
    """Event model."""

    organizer_id: int
    title: str
    description: str
    date: datetime
    is_public: bool
    event_id: int


@router.get("")
def get_events() -> list[EventReturn]:
    """
    Get all events.
    """
    response = httpx.get("http://backend-events:8000/events")
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@router.get("/{event_id}")
def get_event(event_id: int) -> EventReturn:
    """
    Get event.

    Args:
        event_id (int): event id

    Returns:
        EventReturn: event
    """
    response = httpx.get(f"http://backend-events:8000/events/{event_id}")
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@router.post("")
def create_event(event: Event) -> EventReturn:
    """
    Create event.

    Args:
        event (Event): event

    Returns:
        EventReturn: event
    """
    # Additonal validation of organizer_id
    response = httpx.get(f"http://backend-auth:8000/users/{event.organizer_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    response = httpx.post("http://backend-events:8000/events", json={
        "organizer_id": event.organizer_id,
        "title": event.title,
        "description": event.description,
        "date": event.date,
        "is_public": event.is_public,
    })
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
