from fastapi import APIRouter, Body
from starlette import status

from app.enums import UserRole
from app.schemas.users import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users() -> User:
    return User(email="", password="", role=UserRole.ADMIN)


@router.post("/")
async def create_user(user: User = Body(...)):
    return {"message": "User created", "status": status.HTTP_200_OK, "user": user}


@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}
