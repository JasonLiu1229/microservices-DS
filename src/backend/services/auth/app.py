"""
FastAPI application for the auth service.
"""
import auth
import healthcheck
from fastapi import FastAPI

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(healthcheck.router, prefix="/health", tags=["health_check"])
