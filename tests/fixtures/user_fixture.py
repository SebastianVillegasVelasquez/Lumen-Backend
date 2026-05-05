import pytest

from src.model import User
from src.service import UserService


class FakeUserRepository():
    async def get_all(self):
        return [
            User(
                user_id=1,
                email="sebastian@gmail.com",
                name="Sebastian",
                last_name="Villegas",
            ),
            User(
                user_id=2,
                email="juan@gmail.com",
                name="Juan",
                last_name="Perez",
            )
        ]


@pytest.fixture
def fake_user_repository():
    return FakeUserRepository()


@pytest.fixture
def fake_user_service(fake_user_repository):
    from src.service.user.user_service import UserService
    return UserService(fake_user_repository)


class EmptyFakeUserRepository:
    async def get_all(self):
        return []


@pytest.fixture
def empty_fake_user_repository():
    return EmptyFakeUserRepository()


@pytest.fixture
def empty_fake_user_service(empty_fake_user_repository):
    from src.service.user.user_service import UserService
    return UserService(empty_fake_user_repository)


class BrokenFakeUserRepository:
    async def get_all(self):
        raise Exception("Something went wrong")


@pytest.fixture
def broken_fake_user_repository():
    return BrokenFakeUserRepository()


@pytest.fixture
def broken_fake_user_service(broken_fake_user_repository):
    return UserService(broken_fake_user_repository)
