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
    invitee_id: int


class InviteReturn(BaseModel):
    """Invite model."""

    user_id: int
    event_id: int
    invitee_id: int
    status: str
    invite_id: int


@router.get("")
def get_invites() -> list[InviteReturn]:
    """get all invites.

    Returns:
        list[InviteReturn]: list of all invites
    """
    try:
        wrapper = Wrapper()
        invites = wrapper.get_invitations()
        return [
            {
                "user_id": getattr(invite, "user_id"),
                "event_id": getattr(invite, "event_id"),
                "invitee_id": getattr(invite, "invitee_id"),
                "status": getattr(invite, "status"),
                "invite_id": getattr(invite, "id"),
            }
            for invite in invites
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.put("/{invite_id}/status/{status}")
def update_invite_status(invite_id: int, status: str) -> None:
    """
    Update invite status.

    Args:
        invite_id (int): invite id
        status (str): invite status, can be "pending", "accepted", "declined" or "maybe"
        user_id (int): user id
    """
    try:
        wrapper = Wrapper()
        wrapper.update_invitation(invitation_id=invite_id, status=status)
        return Response(status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("")
def create_invite(invite: Invite) -> InviteReturn:
    """
    Create invite.

    Args:
        invite (Invite): invite

    Returns:
        InviteReturn: invite
    """
    try:
        wrapper = Wrapper()

        response = httpx.get(f"http://backend-auth:8000/users/{invite.user_id}")
        if response.status_code != 200:
            return HTTPException(status_code=404, detail="User not found")

        response = httpx.get(f"http://backend-events:8000/events/{invite.event_id}")
        if response.status_code != 200:
            return HTTPException(status_code=404, detail="Event not found")
        else:
            invitation_return = wrapper.create_invitation(
                user_id=invite.user_id,
                event_id=invite.event_id,
                invitee_id=invite.invitee_id,
            )
            return {
                "user_id": getattr(invitation_return, "user_id"),
                "event_id": getattr(invitation_return, "event_id"),
                "invitee_id": getattr(invitation_return, "invitee_id"),
                "status": getattr(invitation_return, "status"),
                "invite_id": getattr(invitation_return, "id"),
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
