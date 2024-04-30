from fastapi import APIRouter, Response

router = APIRouter(responses={404: {"description": "Not found"}})

@router.get("")
async def healthcheck() -> Response:
    """Healthcheck endpoint.

    Returns:
        Response: 200 OK
    """
    return Response(status_code=200)
