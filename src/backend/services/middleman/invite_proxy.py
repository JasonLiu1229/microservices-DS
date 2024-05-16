import httpx
from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import BaseModel

router = APIRouter(responses={404: {"description": "Not found"}})


class Invite(BaseModel):
    """Invite model."""

    user_id: int
    event_id: int
    invitee_id: int


class InviteReturn(BaseModel):
    """Invite model."""

    user_id: int
    event_id: int
    invitee_id: int
    status: str
    invite_id: int


@router.get("/{invite_id}")
def get_invite(invite_id: int) -> InviteReturn:
    """Get invite.

    Args:
        invite_id (int): invite id

    Returns:
        InviteReturn: invite
    """
    response = httpx.get(f"http://backend-invitations:8000/invitations/{invite_id}")
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@router.get("")
def get_invites_route(
    user_id: int = Query(None, description="user id", required=False),
    event_id: int = Query(None, description="event id", required=False),
) -> list[InviteReturn]:
    """
    Get all invites.

    Args:
        user_id (int): user id
        event_id (int): event id

    Returns:
        list[InviteReturn]: list of all invites
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
        response = httpx.get(
            f"http://backend-invitations:8000/invitations?user_id={user_id}&event_id={event_id}"
        )
    elif user_id:
        response = httpx.get(
            f"http://backend-invitations:8000/invitations?user_id={user_id}"
        )
    elif event_id:
        response = httpx.get(
            f"http://backend-invitations:8000/invitations?event_id={event_id}"
        )
    else:
        response = httpx.get("http://backend-invitations:8000/invitations")

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@router.put("/{invite_id}/status/{status}")
def update_invite_status(invite_id: int, status: str) -> None:
    """
    Update invite status.

    Args:
        invite_id (int): invite id
        status (str): invite status, can be "pending", "accepted", "declined" or "maybe"
        user_id (int): user id
    """
    response = httpx.put(
        f"http://backend-invitations:8000/invitations/{invite_id}/status/{status}"
    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return Response(status_code=200)


@router.post("")
def create_invite(invite: Invite) -> InviteReturn:
    """
    Create invite.

    Args:
        invite (Invite): invite

    Returns:
        InviteReturn: invite
    """
    # check if user exists
    response = httpx.get(f"http://backend-auth:8000/users/{invite.user_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    # check if event exists
    response = httpx.get(f"http://backend-events:8000/events/{invite.event_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    # check if invitee exists
    response = httpx.get(f"http://backend-auth:8000/users/{invite.invitee_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    response = httpx.post(
        "http://backend-invitations:8000/invitations",
        json={
            "user_id": invite.user_id,
            "event_id": invite.event_id,
            "invitee_id": invite.invitee_id,
        },
    )
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
