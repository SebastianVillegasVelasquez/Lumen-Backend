from typing import Generic, TypeVar

T = TypeVar("T")


class FakeBaseRepository(Generic[T]):
    """In-memory fake that satisfies RepositoryCrudInterface[T].

    Concrete fakes inherit from this and only need to supply the model's
    primary-key accessor via ``_get_id`` and ``_set_id``.

    Why not inherit from RepositoryCrudInterface?
    Protocol is a static-typing construct. Inheriting from it works at
    runtime, but it is semantically wrong: a Protocol describes a
    *shape*, not a base class. Satisfy it structurally (matching method
    signatures) rather than via inheritance.

    Attributes:
        items: In-memory list acting as the fake "database table".
        exception: If set, every method raises this before doing anything.
    """

    def __init__(
        self,
        items: list[T] | None = None,
        exception: Exception | None = None,
    ) -> None:
        """Initialize the fake repository.

        Args:
            items: Pre-populated rows. Defaults to an empty list.
            exception: Optional error to raise on every call, used to
                simulate database failures.
        """
        self.items: list[T] = items or []
        self.exception = exception

    def _get_id(self, item: T) -> int | None:
        """Return the primary-key value of *item*.

        Args:
            item: ORM-like entity instance.

        Returns:
            Integer primary key, or None if not yet assigned.
        """
        raise NotImplementedError

    def _set_id(self, item: T, id: int) -> None:
        """Assign a primary-key value to *item*.

        Args:
            item: ORM-like entity instance.
            id: Primary key to assign.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _raise_if_needed(self) -> None:
        """Raise the configured exception if one has been set."""
        if self.exception:
            raise self.exception

    def _next_id(self) -> int:
        """Generate the next auto-increment primary key.

        Returns:
            One more than the current maximum id, or 1 for an empty table.
        """
        if not self.items:
            return 1
        return max(self._get_id(item) or 0 for item in self.items) + 1

    # ------------------------------------------------------------------
    # RepositoryCrudInterface implementation
    # ------------------------------------------------------------------

    async def create(self, data: T) -> T:
        """Append *data* to the in-memory list and assign a fake id.

        Args:
            data: Entity instance to persist.

        Returns:
            The same instance with a primary key assigned.
        """
        self._raise_if_needed()

        if self._get_id(data) is None:
            self._set_id(data, self._next_id())

        self.items.append(data)
        return data

    async def get_all(self) -> list[T]:
        """Return all in-memory entities.

        Returns:
            Shallow copy of the internal list.
        """
        self._raise_if_needed()
        return list(self.items)

    async def get_by_id(self, id: int) -> T | None:
        """Find an entity by primary key.

        Args:
            id: Primary key to look up.

        Returns:
            Matching entity, or None if absent.
        """
        self._raise_if_needed()
        return next(
            (item for item in self.items if self._get_id(item) == id),
            None,
        )

    async def save(self, data: T) -> T:
        """Simulate a commit — returns the entity unchanged.

        Args:
            data: Entity to "save".

        Returns:
            The same entity instance.
        """
        self._raise_if_needed()
        return data

    async def soft_delete(self, data: T) -> bool:
        """Set ``is_active = False`` on the entity.

        Args:
            data: Entity to deactivate.

        Returns:
            True on success.
        """
        self._raise_if_needed()
        data.is_active = False  # type: ignore[attr-defined]
        return True
