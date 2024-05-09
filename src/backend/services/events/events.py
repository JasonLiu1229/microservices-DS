# Imports
from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel

from wrapper import Wrapper

router = APIRouter(responses={404: {"description": "Not found"}})


class Event(BaseModel):
    organizer_id: int
    title: str
    description: str
    date: str
    is_public: bool


@router.get("")
def get_events() -> list[dict]:
    """
    Get all events.
    """
    try:
        wrapper = Wrapper()
        events = wrapper.get_events()
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/{event_id}")
def get_event(event_id: int) -> dict:
    """
    Get event.
    """
    try:
        wrapper = Wrapper()
        event = wrapper.get_event(event_id)
        return event
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("")
def create_event(event: Event) -> None:
    """
    Create event.
    """
    try:
        wrapper = Wrapper()
        wrapper.create_event(
            organizer_id=event.organizer_id,
            title=event.title,
            description=event.description,
            date=event.date,
            is_public=event.is_public,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
