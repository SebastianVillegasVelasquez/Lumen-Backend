from typing import Generic, Protocol, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model import User

T = TypeVar("T")


class RepositoryCrudInterface(Protocol[T]):
    """Contract for basic CRUD repository operations.

    Any repository passed to BaseCrudService must satisfy
    this protocol at static-analysis time.
    """

    async def create(self, data: T) -> T:
        """Persist a new entity and return it."""
        ...

    async def get_all(self) -> list[T]:
        """Return all persisted entities."""
        ...

    async def get_by_id(self, id: int) -> T | None:
        """Return the entity with the given primary key, or None."""
        ...

    async def save(self, data: T) -> T:
        """Flush pending changes and refresh the entity."""
        ...

    async def soft_delete(self, data: T) -> bool:
        """Mark the entity as inactive without removing it from the DB.

        Args:
            data: The ORM instance to deactivate.

        Returns:
            True when the operation succeeds.
        """
        ...


class BaseRepository(Generic[T]):
    """Generic SQLAlchemy async repository.

    Provides reusable persistence logic so concrete repositories
    only need to supply entity-specific behaviour.

    Attributes:
        db: The active async database session.
        model: The SQLAlchemy ORM model class.
    """

    def __init__(self, db: AsyncSession, model: Type[T]) -> None:
        """Initialize the repository with a session and model class.

        Args:
            db: Active async SQLAlchemy session.
            model: ORM model class managed by this repository.
        """
        self.db = db
        self.model = model

    async def create(self, data: T) -> T:
        """Add a new entity to the session.

        Args:
            data: ORM instance to persist.

        Returns:
            The same ORM instance after being added to the session.
        """
        self.db.add(data)
        await self.save(data)
        return data

    async def get_all(self) -> list[T]:
        """Retrieve all rows for this model.

        Returns:
            List of ORM instances.
        """
        result = await self.db.execute(select(self.model))
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> T | None:
        """Retrieve a single entity by primary key.

        Args:
            id: Primary key value.

        Returns:
            ORM instance if found, otherwise None.
        """
        return await self.db.get(self.model, id)

    async def save(self, data: T) -> T:
        """Commit the current transaction and refresh the entity.

        Rolls back automatically on failure.

        Args:
            data: ORM instance to refresh after commit.

        Returns:
            The refreshed ORM instance.

        Raises:
            Exception: Re-raises any database error after rolling back.
        """
        try:
            await self.db.commit()
            await self.db.refresh(data)
            return data
        except Exception:
            print("Error saving data")
            await self.db.rollback()
            raise

    async def soft_delete(self, data: T) -> bool:
        """Deactivate an entity without deleting it from the database.

        Args:
            data: ORM instance to deactivate.

        Returns:
            True when the operation succeeds.
        """
        data.is_active = False  # type: ignore[attr-defined]
        await self.save(data)
        return True


class UserCrudRepository(BaseRepository[User]):
    """Concrete repository for User entities."""

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, User)
