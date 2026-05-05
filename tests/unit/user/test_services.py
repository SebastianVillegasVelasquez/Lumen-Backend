import pytest

from src.service import UserService


class TestUserService:
    @pytest.mark.asyncio
    async def test_get_all_users(self, fake_user_service: UserService):
        result = await fake_user_service.get_all_users()
        assert len(result) == 2
        assert result[0].name == "Sebastian"
        assert result[1].name == "Juan"

    @pytest.mark.asyncio
    async def test_get_all_users_empty(self, empty_fake_user_service):
        service = empty_fake_user_service
        users = await service.get_all_users()
        assert len(users) == 0

    @pytest.mark.asyncio
    async def test_get_user_all_users_raise_exception(self, broken_fake_user_service):
        with pytest.raises(Exception):
            await broken_fake_user_service.get_all_users()
