from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from data import UserRepository
from src.db.database import get_db
from src.schema import UserCreate, UserResponse, UserPatch
from src.service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all users from the database.

    Args:
        db (AsyncSession): An instance of AsyncSession for database operations.

    Returns:
        list[UserResponse]: A list of UserResponse objects representing the users.
    """
    repository = UserRepository(db)
    users = await UserService(repository).get_all_users()

    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(
        user: UserCreate = Body(...), db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    This endpoint handles the request to create a new user.

    Args:
        user (UserCreate): User object to be created.
        db (AsyncSession): An instance of AsyncSession for database operations.
    Returns:
        UserResponse: An instance of UserResponse object.

    """

    repository = UserRepository(db)
    user_service = UserService(repository)

    user_created = await user_service.create_user(user_data=user)

    return user_created


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    summary="Get user by ID",
)
async def get_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """
    Retrieve a user by its unique identifier.

    Args:
        user_id (int): Unique identifier of the user.
        db (AsyncSession): Database session dependency.

    Returns:
        UserResponse: User information.

    Raises:
        HTTPException: If the user does not exist.
    """
    repository = UserRepository(db)

    return await UserService(repository).get_user_by_id(user_id)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=str,
    summary="Delete user",
)
async def delete_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
) -> str:
    """
    Soft delete a user by its unique identifier.

    Args:
        user_id (int): Unique identifier of the user.
        db (AsyncSession): Database session dependency.

    Returns:
        str: Operation result message.

    Raises:
        HTTPException: If the user does not exist or deletion fails.
    """
    repository = UserRepository(db)
    return await UserService(repository).delete_user_by_id(user_id=user_id)


@router.patch(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    summary="Update user partially",
)
async def update_user(
        user_id: int,
        new_data: UserPatch = Body(...),
        db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """
    Partially update user information.

    Only provided fields will be updated.

    Args:
        user_id (int): Unique identifier of the user.
        new_data (UserPatch): Partial user data.
        db (AsyncSession): Database session dependency.

    Returns:
        UserResponse: Updated user information.

    Raises:
        HTTPException: If the user does not exist.
    """
    repository = UserRepository(db)
    return await UserService(repository).patch_user(
        user_id=user_id,
        new_data=new_data,
    )
