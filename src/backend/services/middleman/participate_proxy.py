import httpx
from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import BaseModel

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
def get_participations_route(
    user_id: int = Query(default=None, required=False),
    event_id: int = Query(default=None, required=False),
) -> list[ParticipationReturn]:
    """
    Get all participations.

    Args:
        user_id (int): user id
        event_id (int): event id

    Returns:
        list[ParticipationReturn]: list of all participations
    """
    if user_id:
        # check if user exists
        response = httpx.get(f"http://backend-auth:8000/users/{user_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    if event_id:
        # check if event exists
        response = httpx.get(f"http://backend-events:8000/events/{event_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
    if user_id and event_id:
        response = httpx.get(f"http://backend-participations:8000/participations?user_id={user_id}&event_id={event_id}")
    elif user_id:
        response = httpx.get(f"http://backend-participations:8000/participations?user_id={user_id}")
    elif event_id:
        response = httpx.get(f"http://backend-participations:8000/participations?event_id={event_id}")
    else:
        response = httpx.get("http://backend-participations:8000/participations")
        
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@router.get("/{participation_id}")
def get_participation(participation_id: int) -> ParticipationReturn:
    """
    Get participation.

    Args:
        participation_id (int): participation id

    Returns:
        ParticipationReturn: participation
    """
    response = httpx.get(f"http://backend-participations:8000/participations/{participation_id}")
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@router.post("")
def create_participation(participation: Participation) -> ParticipationReturn:
    """
    Create participation.

    Args:
        participation (Participation): participation
        
    HTTPExceptions:
        400: Participation already exists

    Returns:
        ParticipationReturn: participation
    """
    # Additonal validation of user_id and event_id
    response = httpx.get(f"http://backend-auth:8000/users/{participation.user_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    response = httpx.get(f"http://backend-events:8000/events/{participation.event_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    # Check if participation already exists
    response = httpx.get(f"http://backend-participations:8000/participations?user_id={participation.user_id}&event_id={participation.event_id}")
    if response.status_code == 200:
        participations = response.json()
        if participations:
            raise HTTPException(status_code=400, detail="Participation already exists")
    
    response = httpx.post("http://backend-participations:8000/participations", json={
        "user_id": participation.user_id,
        "event_id": participation.event_id,
        "status": participation.status,
    })
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@router.put("/{participation_id}/status/{status}")
def update_participation_status(participation_id: int, status: str) -> None:
    """
    Update participation status.

    Args:
        participation_id (int): participation id
        status (str): participation status, can be "accepted", "declined" or "maybe"
    """
    response = httpx.put(
        f"http://backend-participations:8000/participations/{participation_id}/status/{status}"
    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return Response(status_code=200)
