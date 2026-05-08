import pytest
from fastapi import HTTPException

from src.schema import UserResponse
from tests.builders.user_builders import (
    build_users,
    build_user_create
)
from tests.fixtures.user_fixture import MakeUserService


class TestUserService:

    @pytest.mark.asyncio
    async def test_get_all_users_returns_users(
            self,
            make_user_service: MakeUserService,
    ):
        service = make_user_service(users=build_users())

        result = await service.get_all_users()

        assert len(result) == 2
        assert [user.name for user in result] == [
            "Sebastian",
            "Juan",
        ]

    @pytest.mark.asyncio
    async def test_get_all_users_returns_empty_list(
            self,
            make_user_service: MakeUserService,
    ):
        service = make_user_service(users=[])

        result = await service.get_all_users()

        assert result == []

    @pytest.mark.asyncio
    async def test_get_all_users_propagates_repository_error(
            self,
            make_user_service: MakeUserService,
    ):
        service = make_user_service(
            exception=RuntimeError("db error")
        )

        with pytest.raises(RuntimeError, match="db error"):
            await service.get_all_users()

    @pytest.mark.asyncio
    async def test_create_user_returns_user_response(
            self,
            make_user_service: MakeUserService,
    ):
        user_data = build_user_create()
        service = make_user_service()

        result = await service.create_user(user_data)

        assert isinstance(result, UserResponse)
        assert result.name == user_data.name
        assert result.last_name == user_data.last_name
        assert result.email == user_data.email

    @pytest.mark.asyncio
    async def test_get_user_by_id_returns_user(
            self,
            make_user_service: MakeUserService,
    ):
        service = make_user_service(
            users=build_users()
        )

        result = await service.get_user_by_id(1)

        assert result.name == "Sebastian"

    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(
            self,
            make_user_service: MakeUserService,
    ):
        service = make_user_service(users=[])

        with pytest.raises(HTTPException, match="User with id 999 not found"):
            await service.get_user_by_id(999)

    @pytest.mark.asyncio
    async def test_delete_user_soft_deletes(
            self,
            make_user_service: MakeUserService,
    ):
        users = build_users()
        service = make_user_service(users=users)

        result = await service.delete_user(1)

        assert result == "User with id 1 was deleted"
        assert users[0].is_active is False

    @pytest.mark.asyncio
    async def test_delete_user_soft_deletes_not_found(
            self,
            make_user_service: MakeUserService,
    ):
        service = make_user_service(users=[])

        with pytest.raises(HTTPException, match="User with id 1 not found"):
            await service.delete_user(1)
