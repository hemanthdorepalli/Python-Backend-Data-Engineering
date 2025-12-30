from fastapi import FastAPI
from api.routers import status

app = FastAPI(title="Python Backend Assignment")

app.include_router(status.router)
