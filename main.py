from fastapi import FastAPI
from app.api.routes import example

app = FastAPI()

app.include_router(example.router)
