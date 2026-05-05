import pytest
from pydantic import ValidationError

from src.enums import UserRole
from src.schema import UserCreate, UserPatch


class TestUser:
    def test_user_valid(self, load_fake_user: UserCreate):
        user = load_fake_user
        assert user.email == "jhondoe@example.com"
        assert user.name == "Jhon"
        assert user.last_name == "Doe"
        assert user.password == "securepassword"
        assert user.role == UserRole.STUDENT
        assert user.recovery_email is None

    def test_strip_fiel(self, load_fake_user: UserCreate):
        data = load_fake_user.model_dump()
        data["name"] = "  Juan  "
        assert UserCreate.model_validate(data).name == "Juan"

    def test_user_invalid_role(self, load_fake_user: UserCreate):
        user_dict = load_fake_user.model_dump()
        user_dict["role"] = "invalid_role"
        with pytest.raises(ValidationError):
            UserCreate.model_validate(user_dict)

    def test_invalid_email(self, load_fake_user: UserCreate):
        user_dict = load_fake_user.model_dump()
        user_dict["email"] = "jhondoeexample.com"
        with pytest.raises(ValidationError):
            UserCreate.model_validate(user_dict)

    def test_password_too_short(self, load_fake_user: UserCreate):
        user_dict = load_fake_user.model_dump()
        user_dict["password"] = "123"
        with pytest.raises(ValidationError):
            UserCreate.model_validate(user_dict)

    def test_name_too_short(self, load_fake_user: UserCreate):
        user_dict = load_fake_user.model_dump()
        user_dict["name"] = "J"
        with pytest.raises(ValidationError):
            UserCreate.model_validate(user_dict)

    def test_name_min_length_boundary(self, load_fake_user: UserCreate):
        user_dict = load_fake_user.model_dump()
        user_dict["name"] = "Jo"
        assert UserCreate.model_validate(user_dict).name == "Jo"

    def test_optional_recovery_email(self, load_fake_user: UserCreate):
        expected = None
        assert load_fake_user.recovery_email == expected


class TestUserPatch:
    @pytest.mark.parametrize(
        "payload",
        [
            {"name": "Juan"},
            {"last_name": "Perez"},
            {"email": "juan@gmail.com"},
            {"name": "Juan", "last_name": "Perez"},
            {"last_name": "Perez", "email": "juan@gmail.com"},
        ],
        ids=[
            "patch_name",
            "patch_last_name",
            "patch_email",
            "patch_name_and_last_name",
            "patch_last_name_and_email",
        ],
    )
    def test_patch_only_sent_fields(self, payload):
        user_patch = UserPatch(**payload)

        data = user_patch.model_dump(exclude_unset=True)

        assert data == payload

    def test_patch_empty(self):
        user_patch = UserPatch()
        assert user_patch.model_dump(exclude_unset=True) == {}

    def test_patch_invalid_email(self):
        with pytest.raises(ValidationError):
            UserPatch(email="invalid_email")

    def test_patch_invalid_name(self):
        with pytest.raises(ValidationError):
            UserPatch(name="i")

    def test_patch_invalid_last_name(self):
        with pytest.raises(ValidationError):
            UserPatch(last_name="i")

    def test_patch_invalid_field(self):
        with pytest.raises(ValidationError):
            UserPatch(role=UserRole.STUDENT)

    def test_strip_name(self):
        user_patch = UserPatch(name="  Juan  ")
        assert user_patch.name == "Juan"
