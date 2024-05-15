"""
FastAPI application for the service.
"""

import healthcheck
import participate
from fastapi import FastAPI

app = FastAPI()

app.include_router(healthcheck.router, prefix="/health", tags=["health_check"])
app.include_router(participate.router, prefix="/participations", tags=["participations"])
