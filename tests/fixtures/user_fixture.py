from typing import Protocol

import pytest

from src.model import User
from src.service import UserService


class UserRepositoryProtocol(Protocol):
    async def get_all(self) -> list[User]: ...
    async def add(self, user: User) -> User: ...
    async def save(self, user: User) -> User: ...
    async def get_by_id(self, user_id: int) -> User | None: ...
    async def soft_delete(self, user: User) -> None: ...


class FakeUserRepository(UserRepositoryProtocol):
    def __init__(
        self,
        users: list[User] | None = None,
        exception: Exception | None = None,
    ):
        self.users = users or []
        self.exception = exception

    def _raise_if_needed(self):
        if self.exception:
            raise self.exception

    async def get_all(self) -> list[User]:
        self._raise_if_needed()
        return self.users

    async def add(self, user: User) -> User:
        self._raise_if_needed()

        if user.user_id is None:
            next_id = len(self.users) + 1
            user.user_id = next_id

        self.users.append(user)
        return user

    async def save(self, user: User) -> User:
        self._raise_if_needed()
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        self._raise_if_needed()

        return next(
            (user for user in self.users if user.user_id == user_id),
            None,
        )

    async def soft_delete(self, user: User) -> None:
        self._raise_if_needed()
        user.is_active = False


class MakeUserService(Protocol):
    def __call__(
        self,
        users: list[User] | None = None,
        exception: Exception | None = None,
    ) -> UserService: ...


@pytest.fixture
def make_user_service() -> MakeUserService:
    def _make(
        users: list[User] | None = None,
        exception: Exception | None = None,
    ) -> UserService:
        repo = FakeUserRepository(
            users=users,
            exception=exception,
        )

        return UserService(repo)

    return _make
