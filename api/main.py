from fastapi import FastAPI
from api.routers import status, users
from api.config.database import Base, engine

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Python Backend Assignment")

app.include_router(status.router)
app.include_router(users.router)
