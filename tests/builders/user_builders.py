from src.model import User
from src.schema import UserCreate
from src.enums import UserRole


def build_user(**overrides) -> User:
    data = {
        "user_id": 1,
        "email": "sebastian@gmail.com",
        "name": "Sebastian",
        "last_name": "Villegas",
        "is_active": True,
    }

    data.update(overrides)

    return User(**data)


def build_users() -> list[User]:
    return [
        build_user(),
        build_user(
            user_id=2,
            email="juan@gmail.com",
            name="Juan",
            last_name="Perez",
        ),
    ]


def build_user_create(**overrides) -> UserCreate:
    data = {
        "email": "jhondoe@example.com",
        "recovery_email": None,
        "name": "Jhon",
        "last_name": "Doe",
        "password": "securepassword",
        "role": UserRole.STUDENT,
    }

    data.update(overrides)

    return UserCreate(**data)