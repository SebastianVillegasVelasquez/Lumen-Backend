from fastapi import FastAPI

from src.api.routes.users import user_api
from src.api.routes.health_check import health_check

app = FastAPI()

"""
All the routes are coming from the src.api.routes package.
Do not change the order of the routes, as it may cause issues with the routing.
Do not add any routes here, unless you know what you are doing.
"""
app.include_router(user_api.router)
app.include_router(health_check.router)
