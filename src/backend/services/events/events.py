# Imports
from datetime import datetime

import httpx
from fastapi import APIRouter, HTTPException

from models import EventModel
from pydantic import BaseModel, Field

from wrapper import Wrapper

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
    date: str
    is_public: bool
    event_id: int


def event_parser(event: EventModel) -> dict:
    """Parse event.

    Args:
        event (EventModel): event

    Returns:
        dict: parsed event
    """
    return {
        "organizer_id": getattr(event, "organizer_id"),
        "title": getattr(event, "title"),
        "description": getattr(event, "description"),
        "date": str(getattr(event, "date")),
        "is_public": getattr(event, "is_public"),
        "event_id": getattr(event, "id"),
    }


@router.get("")
def get_events() -> list[EventReturn]:
    """
    Get all events.
    
    HttpExceptions:
        500: Internal server error
    
    Returns:
        list[EventReturn]: list of all events
    """
    try:
        wrapper = Wrapper()
        events = wrapper.get_events()
        events_return = [event_parser(event) for event in events]
        return events_return
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/{event_id}")
def get_event(event_id: int) -> EventReturn:
    """
    Get event.

    Args:
        event_id (int): event id
        
    HttpExceptions:
        500: Internal server error

    Returns:
        EventReturn: event
    """
    try:
        wrapper = Wrapper()
        event = wrapper.get_event(event_id)
        return event_parser(event)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("")
def create_event(event: Event) -> EventReturn:
    """
    Create event.

    Args:
        event (Event): event
    
    HttpExceptions:
        500: Internal server error

    Returns:
        EventReturn: event
    """
    try:
        wrapper = Wrapper()
        event_return = wrapper.create_event(
            organizer_id=event.organizer_id,
            title=event.title,
            description=event.description,
            date=event.date,
            is_public=event.is_public,
        )
        return event_parser(event_return)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
