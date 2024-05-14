# Imports
from datetime import datetime

import httpx
from fastapi import APIRouter, HTTPException

from models import EventModel
from pydantic import BaseModel

from wrapper import Wrapper

router = APIRouter(responses={404: {"description": "Not found"}})


class Event(BaseModel):
    """Event model."""

    organizer_id: int
    title: str
    description: str
    date: str
    is_public: bool


class EventReturn(BaseModel):
    """Event model."""

    organizer_id: int
    title: str
    description: str
    date: datetime
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
        "date": getattr(event, "date"),
        "is_public": getattr(event, "is_public"),
        "event_id": getattr(event, "id"),
    }


@router.get("")
def get_events() -> list[EventReturn]:
    """
    Get all events.
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

    Returns:
        EventReturn: event
    """
    try:
        wrapper = Wrapper()
        # Check if organizer exists
        response = httpx.get(f"http://backend-auth:8000/users/{event.organizer_id}")
        # Convert date to datetime object
        try:
            # Day/month/year
            event.date = datetime.strptime(event.date, "%d/%m/%Y")
        except ValueError as e:
            raise HTTPException(status_code=400, detail="Invalid date format") from e

        if response.status_code != 200:
            return HTTPException(status_code=404, detail="User not found")
        else:
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
