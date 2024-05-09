"""
FastAPI application for the service.
"""
import healthcheck
import invite
from fastapi import FastAPI

app = FastAPI()

app.include_router(healthcheck.router, prefix="/health", tags=["health_check"])
app.include_router(invite.router, prefix="/invitations", tags=["invite"])
