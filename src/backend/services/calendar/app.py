"""
FastAPI application for the service.
"""

import calendar_share
import healthcheck
from fastapi import FastAPI

app = FastAPI()

app.include_router(healthcheck.router, prefix="/health", tags=["health_check"])
app.include_router(calendar_share.router, prefix="/calendars", tags=["calendars"])
