"""
FastAPI application for the service.
"""
import healthcheck
from fastapi import FastAPI

app = FastAPI()

app.include_router(healthcheck.router, prefix="/health", tags=["health_check"])

