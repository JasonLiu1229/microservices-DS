import httpx
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel

router = APIRouter(responses={404: {"description": "Not found"}})
