# Imports
import httpx
from fastapi import APIRouter, HTTPException, Query, Response
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


@router.get("/{invite_id}")
def get_invite(invite_id: int) -> InviteReturn:
    """Get invite.

    Args:
        invite_id (int): invite id

    Returns:
        InviteReturn: invite
    """
    try:
        invite = Wrapper().get_invitation(invite_id)
        return {
            "user_id": getattr(invite, "user_id"),
            "event_id": getattr(invite, "event_id"),
            "invitee_id": getattr(invite, "invitee_id"),
            "status": getattr(invite, "status"),
            "invite_id": getattr(invite, "id"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

def get_invites() -> list[InviteReturn]:
    """get all invites.

    Returns:
        list[InviteReturn]: list of all invites
    """
    try:
        wrapper = Wrapper()
        invites = wrapper.get_all_invitations()
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

def get_invitations_user(user_id: int) -> list[InviteReturn]:
    """Get all invitations.

    Args:
        user_id (int): user id

    Returns:
        list[InviteReturn]: list of invitations
    """
    try:
        wrapper = Wrapper()
        
        invitations = wrapper.get_invitations_by_user(user_id)
        return [
            {
                "user_id": getattr(invitation, "user_id"),
                "event_id": getattr(invitation, "event_id"),
                "invitee_id": getattr(invitation, "invitee_id"),
                "status": getattr(invitation, "status"),
                "invite_id": getattr(invitation, "id"),
            }
            for invitation in invitations
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


def get_invitations_event(event_id: int) -> list[InviteReturn]:
    """Get all invitations.

    Args:
        event_id (int): event id

    Returns:
        list[InviteReturn]: list of invitations
    """
    try:
        wrapper = Wrapper()
        
        invitations = wrapper.get_invitations_by_event(event_id)
        return [
            {
                "user_id": getattr(invitation, "user_id"),
                "event_id": getattr(invitation, "event_id"),
                "invitee_id": getattr(invitation, "invitee_id"),
                "status": getattr(invitation, "status"),
                "invite_id": getattr(invitation, "id"),
            }
            for invitation in invitations
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


def get_invitations_user_event(invitee_id: int, event_id: int) -> InviteReturn:
    """Get all invitations.

    Args:
        invitee_id (int): invitee id
        event_id (int): event id

    Returns:
        list[InviteReturn]: list of invitations
    """
    try:
        wrapper = Wrapper()
        
        invitation = wrapper.get_invitations_by_user_event(invitee_id, event_id)
        return {
            "user_id": getattr(invitation, "user_id"),
            "event_id": getattr(invitation, "event_id"),
            "invitee_id": getattr(invitation, "invitee_id"),
            "status": getattr(invitation, "status"),
            "invite_id": getattr(invitation, "id"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

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
    
    HttpExceptions:
        500: Internal server error

    Returns:
        list[InviteReturn]: list of all invites
    """
    try:
        if user_id and event_id:
            return [get_invitations_user_event(user_id, event_id)]
        elif user_id:
            return get_invitations_user(user_id)
        elif event_id:
            return get_invitations_event(event_id)
        return get_invites()
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
    
    HttpExceptions:
        500: Internal server error
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
    
    HttpExceptions:
        500: Internal server error

    Returns:
        InviteReturn: invite
    """
    try:
        wrapper = Wrapper()

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
