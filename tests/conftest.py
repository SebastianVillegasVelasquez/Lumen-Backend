import pytest

from src.schema import UserCreate
from tests.builders.user_builders import build_user_create

pytest_plugins = [
    "tests.fixtures.model_fixtures",
]


@pytest.fixture
def load_fake_user() -> UserCreate:
    """Load a fake UserCreate instance for schema tests.

    Returns:
        A pre-configured UserCreate DTO with default test values.
    """
    return build_user_create(
        name="Jhon",
        last_name="Doe",
        email="jhondoe@example.com",
        password="securepassword",
    )
