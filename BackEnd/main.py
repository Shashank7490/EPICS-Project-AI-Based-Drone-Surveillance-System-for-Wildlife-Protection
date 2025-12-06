from fastapi import FastAPI
from app.api.routes import drones, users
from app.database.db import engine
from app.database import models

app = FastAPI()

# Register routers for drones and users
app.include_router(drones.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Hello World"}

# Automatically create all tables at startup
models.Base.metadata.create_all(bind=engine)



