from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model import User


class UserRepository:
    """
    Repository layer responsible for database access.

    This class handles all persistence operations related
    to the User entity.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Initialize repository.

        Args:
            db (AsyncSession): SQLAlchemy async session.
        """
        self.db = db

    async def save(self, user: User) -> User:
        """
        Persist changes to the database.

        Args:
            user (User): User entity to save.

        Returns:
            User: Persisted user entity.

        Raises:
            Exception: Re-raises database exception after rollback.
        """
        try:
            await self.db.commit()
            await self.db.refresh(user)

            return user

        except Exception:
            await self.db.rollback()
            raise

    async def add(self, user: User) -> User:
        """
        Add a new user to the database.

        Args:
            user (User): User entity.

        Returns:
            User: Persisted user entity.
        """
        self.db.add(user)

        await self.save(user)

        return user

    async def get_all(self) -> list[User]:
        """
        Retrieve all users.

        Returns:
            list[User]: List of users.
        """
        query = select(User)

        result = await self.db.execute(query)

        return result.scalars().all()

    async def get_by_id(self, user_id: int) -> User | None:
        """
        Retrieve a user by ID.

        Args:
            user_id (int): User identifier.

        Returns:
            User | None: User entity if found, otherwise None.
        """
        return await self.db.get(User, user_id)

    async def soft_delete(self, user: User) -> None:
        """
        Perform a soft delete.

        Marks the user as inactive instead of deleting
        the record permanently.

        Args:
            user (User): User entity to deactivate.
        """
        user.is_active = False

        await self.save(user)
