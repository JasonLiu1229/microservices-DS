# Imports
import httpx
from fastapi import APIRouter, HTTPException, Response
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


@router.get("")
def get_events() -> list[dict]:
    """
    Get all events.
    """
    try:
        wrapper = Wrapper()
        events = wrapper.get_events()
        return Response(status_code=200, content=events)
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
        return Response(status_code=200, content=event)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("")
def create_event(event: Event) -> None:
    """
    Create event.
    """
    try:
        wrapper = Wrapper()
        # Check if organizer exists
        response = httpx.get(f"http://backend-auth:8000/users/{event.organizer_id}")
        if response.status_code != 200:
            return Response(status_code=404, content="Organizer not found")
        else:
            wrapper.create_event(
                organizer_id=event.organizer_id,
                title=event.title,
                description=event.description,
                date=event.date,
                is_public=event.is_public,
            )
            return Response(status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
