# Imports
import httpx
from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import BaseModel

from wrapper import Wrapper

router = APIRouter(responses={404: {"description": "Not found"}})


class Participation(BaseModel):
    """Participation model."""

    user_id: int
    event_id: int
    status: str


class ParticipationReturn(BaseModel):
    """Participation model."""

    user_id: int
    event_id: int
    status: str
    participation_id: int


def get_particpations() -> list[ParticipationReturn]:
    """
    Get all participations.

    Returns:
        list[ParticipationReturn]: list of all participations
    """
    try:
        wrapper = Wrapper()
        participations = wrapper.get_all_participations()
        return [
            {
                "user_id": getattr(participation, "user_id"),
                "event_id": getattr(participation, "event_id"),
                "status": getattr(participation, "status"),
                "participation_id": getattr(participation, "id"),
            }
            for participation in participations
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


def get_participations_by_event(event_id: int) -> list[ParticipationReturn]:
    """
    Get all participations by event.

    Args:
        event_id (int): event id

    Returns:
        list[ParticipationReturn]: list of all participations by event
    """
    try:
        wrapper = Wrapper()
        participations = wrapper.get_participations_by_event(event_id)
        return [
            {
                "user_id": getattr(participation, "user_id"),
                "event_id": getattr(participation, "event_id"),
                "status": getattr(participation, "status"),
                "participation_id": getattr(participation, "id"),
            }
            for participation in participations
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


def get_participations_by_user_event(
    user_id: int, event_id: int
) -> ParticipationReturn:
    """
    Get participation by user and event.

    Args:
        user_id (int): user id
        event_id (int): event id

    Returns:
        ParticipationReturn: participation
    """
    try:
        wrapper = Wrapper()
        participation = wrapper.get_participations_by_user_event(
            user_id=user_id, event_id=event_id
        )
        return {
            "user_id": getattr(participation, "user_id"),
            "event_id": getattr(participation, "event_id"),
            "status": getattr(participation, "status"),
            "participation_id": getattr(participation, "id"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("")
def get_participations_route(
    user_id: int = Query(default=None), event_id: int = Query(default=None)
) -> list[ParticipationReturn]:
    """
    Get all participations.

    Args:
        user_id (int): user id
        event_id (int): event id

    Returns:
        list[ParticipationReturn]: list of all participations
    """
    if user_id is not None and event_id is not None:
        return [get_participations_by_user_event(user_id, event_id)]
    elif event_id is not None:
        return get_participations_by_event(event_id)
    else:
        return get_particpations()


@router.get("/{participation_id}")
def get_participation(participation_id: int) -> ParticipationReturn:
    """
    Get participation.

    Args:
        participation_id (int): participation id

    Returns:
        ParticipationReturn: participation
    """
    try:
        wrapper = Wrapper()
        participation = wrapper.get_participation(participation_id)
        return {
            "user_id": getattr(participation, "user_id"),
            "event_id": getattr(participation, "event_id"),
            "status": getattr(participation, "status"),
            "participation_id": getattr(participation, "id"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("")
def create_participation(participation: Participation) -> ParticipationReturn:
    """
    Create participation.

    Args:
        participation (Participation): participation

    Returns:
        ParticipationReturn: participation
    """
    try:
        wrapper = Wrapper()
        response = httpx.get(f"http://backend-auth:8000/users/{participation.user_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="User not found")
        participate_return = wrapper.create_participation(
            user_id=participation.user_id,
            event_id=participation.event_id,
            status=participation.status,
        )
        return {
            "user_id": getattr(participate_return, "user_id"),
            "event_id": getattr(participate_return, "event_id"),
            "status": getattr(participate_return, "status"),
            "participation_id": getattr(participate_return, "id"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.put("/{participation_id}/status/{status}")
def update_participation_status(participation_id: int, status: str) -> None:
    """
    Update participation status.

    Args:
        participation_id (int): participation id
        status (str): participation status, can be "accepted", "declined" or "maybe"
    """
    try:
        wrapper = Wrapper()
        wrapper.update_participation(participation_id=participation_id, status=status)
        return Response(status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
