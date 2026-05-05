import pytest

from src.schema import UserCreate

pytest_plugins = [
    "tests.fixtures.user_fixture",
]


@pytest.fixture
def load_fake_user() -> UserCreate:
    from src.enums.enums import UserRole

    return UserCreate(
        email="jhondoe@example.com",
        recovery_email=None,
        name="Jhon",
        last_name="Doe",
        password="securepassword",
        role=UserRole.STUDENT,
    )

# User service fixtures
