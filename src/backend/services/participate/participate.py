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
def get_user_participations(user_id: int) -> list[ParticipationReturn]:
    """
    Get user participations.
    """
    try:
        wrapper = Wrapper()
        response = httpx.get(f"http://backend-auth:8000/users/{user_id}")
        if response.status_code != 200:
            return Response(status_code=404, content="User not found")
        participations = wrapper.get_participations(user_id)
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


@router.post("")
def create_participation(participation: Participation) -> None:
    """
    Create participation.
    """
    try:
        wrapper = Wrapper()
        response = httpx.get(f"http://backend-auth:8000/users/{participation.user_id}")
        if response.status_code != 200:
            return Response(status_code=404, content="User not found")
        wrapper.create_participation(
            user_id=participation.user_id,
            event_id=participation.event_id,
            status=participation.status,
        )
        return Response(status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.put("/{participation_id}/status/{status}")
def update_participation_status(participation_id: int, status: str) -> None:
    """
    Update participation status.

    Args:
        participation_id (int): participation id
        status (str): participation status
    """
    try:
        wrapper = Wrapper()
        wrapper.update_participation(participation_id=participation_id, status=status)
        return Response(status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
