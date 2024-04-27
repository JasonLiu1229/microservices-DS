from fastapi import FastAPI
import auth, healthcheck

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(healthcheck.router, prefix="/health", tags=["health_check"])
