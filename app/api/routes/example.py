# app/api/routes/user_routes.py

from fastapi import APIRouter

router = APIRouter(prefix="/users")


@router.get("/")
async def get_users():
    return "List of users"
