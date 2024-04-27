"""
FastAPI application for the auth service.
"""
import auth
import healthcheck
import users
from fastapi import FastAPI

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(healthcheck.router, prefix="/health", tags=["health_check"])
app.include_router(users.router, prefix="/users", tags=["users"])
