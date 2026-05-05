from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.data import UserRepository
from src.model import User
from src.schema import UserCreate, UserPatch, UserResponse


class UserService:
    """
    Service layer responsible for user business logic.

    This class acts as an intermediary between the API layer
    and the repository layer, handling validation, transformations,
    and application rules.
    """

    def __init__(self, repository: UserRepository) -> None:
        """
        Initialize service with database session.

        Args:
            db (AsyncSession): SQLAlchemy async database session.
        """
        self.repository = repository

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """
        Create a new user.

        Args:
            user_data (UserCreate): User creation payload.

        Returns:
            UserResponse: Created user data.
        """
        new_user = self._convert_to_orm_model(user_data)

        user = await self.repository.add(new_user)

        return self._convert_single_user_to_response(user)

    async def get_all_users(self) -> list[UserResponse]:
        """
        Retrieve all users.

        Returns:
            list[UserResponse]: List of users.
        """
        users = await self.repository.get_all()

        return self._convert_users_to_response(users)

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        """
        Retrieve a user by ID.

        Args:
            user_id (int): User identifier.

        Returns:
            UserResponse: User data.

        Raises:
            HTTPException: If user is not found.
        """
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )

        return self._convert_single_user_to_response(user)

    async def delete_user_by_id(self, user_id: int) -> str:
        """
        Soft delete a user by ID.

        The user is marked as inactive instead of being
        physically removed from the database.

        Args:
            user_id (int): User identifier.

        Returns:
            str: Success operation message.

        Raises:
            HTTPException: If user is not found.
            HTTPException: If delete operation fails.
        """
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )

        try:
            await self.repository.soft_delete(user)

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Delete operation failed",
            )

        return f"User with id {user_id} was deleted"

    async def patch_user(
        self,
        user_id: int,
        new_data: UserPatch,
    ) -> UserResponse:
        """
        Partially update a user.

        Only provided fields are updated.

        Args:
            user_id (int): User identifier.
            new_data (UserPatch): Partial update payload.

        Returns:
            UserResponse: Updated user data.

        Raises:
            HTTPException: If user is not found.
        """
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )

        for key, value in new_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)

        updated_user = await self.repository.save(user)

        return self._convert_single_user_to_response(updated_user)

    @staticmethod
    def _convert_to_orm_model(user: UserCreate) -> User:
        """
        Convert schema model into ORM model.

        Args:
            user (UserCreate): Input schema.

        Returns:
            User: ORM entity.
        """
        return User(**user.model_dump())

    @staticmethod
    def _convert_single_user_to_response(user: User) -> UserResponse:
        """
        Convert ORM user into response schema.

        Args:
            user (User): ORM entity.

        Returns:
            UserResponse: Serialized response object.
        """
        return UserResponse.model_validate(user)

    @staticmethod
    def _convert_users_to_response(
        users: list[User],
    ) -> list[UserResponse]:
        """
        Convert ORM user list into response schema list.

        Args:
            users (list[User]): ORM user list.

        Returns:
            list[UserResponse]: Serialized response list.
        """
        return [UserResponse.model_validate(user) for user in users]
