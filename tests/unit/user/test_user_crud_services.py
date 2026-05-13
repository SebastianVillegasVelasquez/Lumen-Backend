from typing import Protocol  # noqa: E402

import pytest

from src.model import User
from src.schema import UserCreate, UserPatch
from src.service import UserCrudService  # noqa: E402
from tests.builders.user_builders import (
    build_user,
    build_users,
    build_user_create,
    build_user_patch,
)
from tests.fixtures.generic import BaseCrudServiceTests
from tests.unit.user.fake_user_repository import FakeUserRepository


class MakeUserCrudService(Protocol):
    """Typing helper for the make_service fixture."""

    def __call__(
        self,
        items: list[User] | None = None,
        exception: Exception | None = None,
    ) -> UserCrudService: ...


class TestUserCrudService(BaseCrudServiceTests):
    """CRUD test suite for UserCrudService.

    All test cases come from BaseCrudServiceTests.
    This class only provides User-specific builders and the fixture.
    """

    # ------------------------------------------------------------------
    # Builders
    # ------------------------------------------------------------------

    def build_entity(self, *, id: int = 1, name: str = "Sebastian", **kwargs) -> User:
        """Build a User ORM instance.

        Args:
            id: Primary key.
            name: First name.
            **kwargs: Additional User field overrides.

        Returns:
            Configured User instance.
        """
        return build_user(user_id=id, name=name, **kwargs)

    def build_entities(self) -> list[User]:
        """Return two pre-built User instances.

        Returns:
            List of two User instances.
        """
        return build_users()

    def build_create_dto(self, **kwargs) -> UserCreate:
        """Build a UserCreate DTO.

        Args:
            **kwargs: Field overrides.

        Returns:
            Configured UserCreate DTO.
        """
        return build_user_create(**kwargs)

    def build_patch_dto(self, **kwargs) -> UserPatch:
        """Build a UserPatch DTO.

        Args:
            **kwargs: Partial field values.

        Returns:
            Configured UserPatch DTO.
        """
        return build_user_patch(**kwargs)

    # ------------------------------------------------------------------
    # Fixture
    # ------------------------------------------------------------------

    @pytest.fixture
    def make_service(self) -> MakeUserCrudService:
        """Provide a factory that creates a UserCrudService with a fake repo.

        Returns:
            Callable that accepts ``items`` and ``exception`` and returns
            a fully wired UserCrudService.
        """

        def _make(
            items: list[User] | None = None,
            exception: Exception | None = None,
        ) -> UserCrudService:
            repo = FakeUserRepository(items=items, exception=exception)
            return UserCrudService(repo)

        return _make
