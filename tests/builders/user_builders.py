from src.enums.enums import UserRole  # noqa: E402
from src.model import User  # noqa: E402
from src.schema import UserCreate, UserPatch  # noqa: E402


def build_user(
    *,
    user_id: int = 1,
    name: str = "Sebastian",
    last_name: str = "Gomez",
    email: str = "sebastian@example.com",
    is_active: bool = True,
) -> User:
    """Construct a User ORM instance with sensible defaults.

    All parameters are keyword-only so call sites are self-documenting.

    Args:
        user_id: Primary key.
        name: First name.
        last_name: Last name.
        email: Email address.
        is_active: Active flag.

    Returns:
        Configured User instance.
    """
    user = User()
    user.user_id = user_id
    user.name = name
    user.last_name = last_name
    user.email = email
    user.is_active = is_active
    return user


def build_users() -> list[User]:
    """Return a small pre-built list of User instances.

    Returns:
        Two distinct User instances for list-based test scenarios.
    """
    return [
        build_user(user_id=1, name="Sebastian", email="seb@example.com"),
        build_user(user_id=2, name="Juan", email="juan@example.com"),
    ]


def build_user_create(
    *,
    name: str = "John",
    last_name: str = "Doe",
    email: str = "john@example.com",
    password: str = "secret123",
    role: UserRole = UserRole.STUDENT,
) -> UserCreate:
    """Construct a UserCreate DTO with sensible defaults.

    Args:
        name: First name.
        last_name: Last name.
        email: Email address.
        password: Plain-text password.
        role: User role enum value.

    Returns:
        Configured UserCreate DTO.
    """
    return UserCreate(
        name=name,
        last_name=last_name,
        email=email,
        recovery_email=None,
        password=password,
        role=role,
    )


def build_user_patch(**kwargs) -> UserPatch:
    """Construct a UserPatch DTO from arbitrary keyword arguments.

    Only the supplied fields are set; all others remain unset so that
    ``model_dump(exclude_unset=True)`` works correctly.

    Args:
        **kwargs: Any subset of UserPatch fields.

    Returns:
        Configured UserPatch DTO.
    """
    return UserPatch(**kwargs)
