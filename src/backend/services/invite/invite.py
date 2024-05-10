# Imports
import httpx
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel

from wrapper import Wrapper

router = APIRouter(responses={404: {"description": "Not found"}})


class Invite(BaseModel):
    """Invite model."""

    user_id: int
    event_id: int
    Invitee_id: int


@router.get("/{user_id}")
def get_user_invite(user_id: int) -> dict:
    """
    Get user pending invites.
    """
    try:
        wrapper = Wrapper()
        response = httpx.get(f"http://backend-auth:8000/users/{user_id}")
        if response.status_code != 200:
            return Response(status_code=404, content="User not found")
        else:
            invites = wrapper.get_invitations(user_id)
            pending_invites = [
                invite for invite in invites if invite["status"] == "pending"
            ]
            return Response(status_code=200, content=pending_invites)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.put("/{invite_id}/status/{status}")
def update_invite_status(invite_id: int, status: str) -> None:
    """
    Update invite status.

    Args:
        invite_id (int): invite id
        status (str): invite status
        user_id (int): user id
    """
    try:
        wrapper = Wrapper()
        wrapper.update_invitation(invitation_id=invite_id, status=status)
        return Response(status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("")
def create_invite(invite: Invite) -> None:
    """
    Create invite.
    """
    try:
        wrapper = Wrapper()
        response = httpx.get(f"http://backend-auth:8000/users/{invite.user_id}")
        if response.status_code != 200:
            return Response(status_code=404, content="User not found")
        response = httpx.get(f"http://backend-events:8000/events/{invite.event_id}")
        if response.status_code != 200:
            return Response(status_code=404, content="Event not found")
        else:
            wrapper.create_invitation(
                user_id=invite.user_id,
                event_id=invite.event_id,
                invitee_id=invite.Invitee_id,
            )
            return Response(status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
