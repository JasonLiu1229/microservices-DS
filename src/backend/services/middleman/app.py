"""
FastAPI application for the service.
"""

import auth_proxy, calendar_proxy, events_proxy, invite_proxy, participate_proxy, users_proxy
import healthcheck
from fastapi import FastAPI

app = FastAPI()

app.include_router(auth_proxy.router, prefix="/auth", tags=["auth"])
app.include_router(events_proxy.router, prefix="/events", tags=["events"])
app.include_router(calendar_proxy.router, prefix="/calendar", tags=["calendar"])
app.include_router(users_proxy.router, prefix="/users", tags=["users"])
app.include_router(
    participate_proxy.router, prefix="/participation", tags=["participation"]
)
app.include_router(invite_proxy.router, prefix="/invitation", tags=["invitation"])
app.include_router(healthcheck.router, prefix="/health", tags=["health_check"])
