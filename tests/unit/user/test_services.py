from typing import Protocol

import pytest

from src.model import User
from src.service import UserService  # noqa: E402
from tests.unit.user.fake_user_repository import FakeUserRepository


class MakeUserService(Protocol):
    """Typing helper for the make_service fixture."""

    def __call__(
        self,
        items: list[User] | None = None,
        exception: Exception | None = None,
    ) -> UserService: ...


class TestUserService:
    """Tests for business logic that lives exclusively in UserService."""

    @pytest.fixture
    def make_service(self) -> MakeUserService:
        """Provide a factory that creates a UserService with a fake repo.

        Returns:
            Callable that accepts ``items`` and ``exception`` and returns
            a fully wired UserService.
        """

        def _make(
            items: list[User] | None = None,
            exception: Exception | None = None,
        ) -> UserService:
            repo = FakeUserRepository(items=items, exception=exception)
            return UserService(repo)

        return _make
