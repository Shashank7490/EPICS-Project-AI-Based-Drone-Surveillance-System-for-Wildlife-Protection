from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Forest Surveillance Backend",
    description="Backend for Multi-Drone Forest Surveillance System",
    version="1.0.0"
)

app.include_router(router)