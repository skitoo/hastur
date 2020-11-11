from fastapi import FastAPI
from .route import router


web_app = FastAPI()
web_app.include_router(router, prefix="/api")
