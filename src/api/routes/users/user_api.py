from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.database import get_db
from src.data import UserCrudRepository
from src.schema import UserCreate, UserPatch, UserResponse
from src.service import UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """Provide a fully wired UserCrudService for the current request.

    FastAPI resolves this via Depends, so every endpoint receives
    a fresh service+repository pair that shares the same db session.

    Args:
        db: Async database session injected by FastAPI.

    Returns:
        Configured UserCrudService instance.
    """
    return UserService(UserCrudRepository(db))


# ------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
async def get_users(
    service: UserService = Depends(get_user_service),
) -> list[UserResponse]:
    """Retrieve all users.

    Returns:
        List of UserResponse objects.
    """
    return await service.get_all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(
    user: UserCreate = Body(...),
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Create a new user.

    Args:
        user: User creation payload.
        service: Injected user service.

    Returns:
        The created UserResponse.
    """
    return await service.create(user)


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Retrieve a user by ID.

    Args:
        user_id: Target user primary key.
        service: Injected user service.

    Returns:
        Matching UserResponse.

    Raises:
        HTTPException: 404 if the user does not exist.
    """
    return await service.get_by_id(user_id)


@router.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_user(
    user_id: int,
    new_data: UserPatch = Body(...),
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Partially update a user.

    Only fields present in the request body are modified.

    Args:
        user_id: Target user primary key.
        new_data: Partial update payload.
        service: Injected user service.

    Returns:
        Updated UserResponse.

    Raises:
        HTTPException: 404 if the user does not exist.
    """
    return await service.patch(user_id, new_data)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK, response_model=bool)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> bool:
    """Soft-delete a user.

    Args:
        user_id: Target user primary key.
        service: Injected user service.

    Returns:
        True when the deletion succeeds.

    Raises:
        HTTPException: 404 if the user does not exist.
    """
    return await service.delete(user_id)
