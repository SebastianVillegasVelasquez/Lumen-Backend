from src.model import User  # noqa: E402
from tests.fixtures.generic import FakeBaseRepository


class FakeUserRepository(FakeBaseRepository[User]):
    """In-memory User repository for unit tests.

    Only overrides the two id-accessor hooks; all CRUD logic is
    inherited from FakeBaseRepository.
    """

    def _get_id(self, item: User) -> int | None:
        """Return the User's primary key.

        Args:
            item: User ORM instance.

        Returns:
            Integer user_id or None.
        """
        return item.user_id

    def _set_id(self, item: User, id: int) -> None:
        """Assign a primary key to a User.

        Args:
            item: User ORM instance.
            id: Primary key to assign.
        """
        item.user_id = id
