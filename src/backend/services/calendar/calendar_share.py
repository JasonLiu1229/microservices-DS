# Imports
from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel

from wrapper import Wrapper

router = APIRouter(responses={404: {"description": "Not found"}})


