"""
FastAPI application for the service.
"""
import healthcheck
import events
from fastapi import FastAPI

app = FastAPI()

app.include_router(healthcheck.router, prefix="/health", tags=["health_check"])
app.include_router(events.router, prefix="/events", tags=["events"])
