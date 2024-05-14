# Imports
import httpx
from fastapi import APIRouter, HTTPException, Response
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


@router.get("")
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
