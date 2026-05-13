import pytest  # noqa: E402
from fastapi import HTTPException  # noqa: E402


class BaseCrudServiceTests:
    """Reusable CRUD test contract.

    Any concrete test class that inherits this and implements the three
    abstract builder methods gets the full CRUD test suite for free.

    How to use
    ----------
    1. Subclass ``BaseCrudServiceTests``.
    2. Implement ``build_entity``, ``build_create_dto``, and
       ``build_patch_dto``.
    3. Define a ``make_service`` pytest fixture that returns a callable
       matching the signature ``(items, exception) -> ConcreteService``.

    pytest will collect every ``test_*`` method automatically.

    Example
    -------
    class TestUserCrudService(BaseCrudServiceTests):
        def build_entity(self, **kwargs): ...
        def build_create_dto(self, **kwargs): ...
        def build_patch_dto(self, **kwargs): ...

        @pytest.fixture
        def make_service(self): ...
    """

    # ------------------------------------------------------------------
    # Abstract builders — subclasses must implement these
    # ------------------------------------------------------------------

    def build_entity(self, **kwargs):
        """Return an ORM entity instance.

        Args:
            **kwargs: Field overrides.
        """
        raise NotImplementedError

    def build_entities(self) -> list:
        """Return a small list of distinct entities for list tests.

        Returns:
            List with at least two entities.
        """
        raise NotImplementedError

    def build_create_dto(self, **kwargs):
        """Return a creation DTO instance.

        Args:
            **kwargs: Field overrides.
        """
        raise NotImplementedError

    def build_patch_dto(self, **kwargs):
        """Return a partial-update DTO instance.

        Args:
            **kwargs: Field overrides.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # get_all
    # ------------------------------------------------------------------

    @pytest.mark.asyncio
    async def test_get_all_returns_all_entities(self, make_service):
        """get_all returns every entity in the repository."""
        entities = self.build_entities()
        service = make_service(items=entities)

        result = await service.get_all()

        assert len(result) == len(entities)

    @pytest.mark.asyncio
    async def test_get_all_returns_empty_list_when_no_entities(self, make_service):
        """get_all returns an empty list when the repository is empty."""
        service = make_service(items=[])

        result = await service.get_all()

        assert result == []

    @pytest.mark.asyncio
    async def test_get_all_propagates_repository_error(self, make_service):
        """get_all re-raises exceptions coming from the repository."""
        service = make_service(exception=RuntimeError("db error"))

        with pytest.raises(RuntimeError, match="db error"):
            await service.get_all()

    # ------------------------------------------------------------------
    # get_by_id
    # ------------------------------------------------------------------

    @pytest.mark.asyncio
    async def test_get_by_id_returns_correct_entity(self, make_service):
        """get_by_id returns the entity matching the given id."""
        entities = self.build_entities()
        service = make_service(items=entities)

        result = await service.get_by_id(1)

        assert result is not None

    @pytest.mark.asyncio
    async def test_get_by_id_raises_404_when_not_found(self, make_service):
        """get_by_id raises HTTP 404 for an unknown id."""
        service = make_service(items=[])

        with pytest.raises(HTTPException) as exc_info:
            await service.get_by_id(999)

        assert exc_info.value.status_code == 404

    # ------------------------------------------------------------------
    # create
    # ------------------------------------------------------------------

    @pytest.mark.asyncio
    async def test_create_returns_response_dto(self, make_service):
        """create persists an entity and returns its response DTO."""
        dto = self.build_create_dto()
        service = make_service()

        result = await service.create(dto)

        assert result is not None

    # ------------------------------------------------------------------
    # patch
    # ------------------------------------------------------------------

    @pytest.mark.asyncio
    async def test_patch_updates_only_supplied_fields(self, make_service):
        """patch updates only the fields present in the payload."""
        entity = self.build_entity(id=1, name="Original")
        service = make_service(items=[entity])
        patch_dto = self.build_patch_dto(name="Updated")

        result = await service.patch(1, patch_dto)

        assert result.name == "Updated"

    @pytest.mark.asyncio
    async def test_patch_raises_404_when_not_found(self, make_service):
        """patch raises HTTP 404 when the target entity does not exist."""
        service = make_service(items=[])
        patch_dto = self.build_patch_dto(name="X")

        with pytest.raises(HTTPException) as exc_info:
            await service.patch(999, patch_dto)

        assert exc_info.value.status_code == 404

    # ------------------------------------------------------------------
    # delete
    # ------------------------------------------------------------------

    @pytest.mark.asyncio
    async def test_delete_soft_deletes_entity(self, make_service):
        """delete marks the entity as inactive without removing it."""
        entity = self.build_entity(id=1)
        service = make_service(items=[entity])

        result = await service.delete(1)

        assert result is True
        assert entity.is_active is False

    @pytest.mark.asyncio
    async def test_delete_raises_404_when_not_found(self, make_service):
        """delete raises HTTP 404 when the target entity does not exist."""
        service = make_service(items=[])

        with pytest.raises(HTTPException) as exc_info:
            await service.delete(999)

        assert exc_info.value.status_code == 404
