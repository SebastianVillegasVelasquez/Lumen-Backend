import pytest
from pydantic import ValidationError

from app.enums.enums import UserRole
from app.schemas.users.user import User


class TestUser:
    def test_user_valid(self, load_fake_user: User):
        user = load_fake_user
        assert user.email == "jhondoe@example.com"
        assert user.name == "Jhon"
        assert user.last_name == "Doe"
        assert user.password == "securepassword"
        assert user.role == UserRole.STUDENT
        assert user.recovery_email is None

    def test_invalid_email(self, load_fake_user: User):
        user_dict = load_fake_user.model_dump()
        user_dict["email"] = "jhondoeexample.com"
        with pytest.raises(ValidationError):
            User.model_validate(user_dict)

    def test_password_too_short(self, load_fake_user: User):
        user_dict = load_fake_user.model_dump()
        user_dict["password"] = "123"
        with pytest.raises(ValidationError):
            User.model_validate(user_dict)

    def test_name_too_short(self, load_fake_user: User):
        user_dict = load_fake_user.model_dump()
        user_dict["name"] = "J"
        with pytest.raises(ValidationError):
            User.model_validate(user_dict)

    def test_name_min_length_boundary(self, load_fake_user: User):
        user_dict = load_fake_user.model_dump()
        user_dict["name"] = "Jo"
        assert User.model_validate(user_dict).name == "Jo"

    def test_optional_recovery_email(self, load_fake_user: User):
        expected = None
        assert load_fake_user.recovery_email == expected
