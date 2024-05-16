"""
FastAPI application for the service.
"""
import auth_proxy
import healthcheck
from fastapi import FastAPI

app = FastAPI()

app.include_router(auth_proxy.router, prefix="/auth", tags=["auth"])
app.include_router(healthcheck.router, prefix="/health", tags=["health_check"])
