"""Generic CRUD service interface with standard operations."""

from __future__ import annotations

from typing import Generic, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status

from src.model import User
from src.schema import UserCreate, UserPatch, UserResponse
from src.data import RepositoryCrudInterface

ModelT = TypeVar("ModelT")
CreateDTO = TypeVar("CreateDTO", bound=BaseModel)
PatchDTO = TypeVar("PatchDTO", bound=BaseModel)
ResponseDTO = TypeVar("ResponseDTO", bound=BaseModel)


class BaseCrudService(
    Generic[
        ModelT,
        CreateDTO,
        PatchDTO,
        ResponseDTO,
    ]
):
    """Generic CRUD service that delegates persistence to a repository.

    Centralizes the 404-guard, DTO↔ORM conversion, and commit
    orchestration so concrete services stay thin.

    Attributes:
        repository: Repository instance that satisfies RepositoryCrudInterface.
        model: ORM model class used for DTO→ORM conversion.
        response_model: Pydantic response class used for ORM→DTO conversion.
    """

    def __init__(
        self,
        repository: RepositoryCrudInterface[ModelT],
        model: type[ModelT],
        response_model: type[ResponseDTO],
    ) -> None:
        """Initialize a service with its dependencies.

        Args:
            repository: Repository implementation for the managed entity.
            model: ORM model class.
            response_model: Pydantic response DTO class.
        """
        self.repository = repository
        self.model = model
        self.response_model = response_model

    # ------------------------------------------------------------------
    # Public CRUD operations
    # ------------------------------------------------------------------

    async def create(self, data: CreateDTO) -> ResponseDTO:
        """Persist a new entity.

        Args:
            data: Creation DTO payload.

        Returns:
            Serialised response DTO for the created entity.
        """
        orm_object = self.convert_to_orm(data)
        saved_object = await self.repository.create(orm_object)
        return self.convert_to_response(saved_object)

    async def get_all(self) -> list[ResponseDTO]:
        """Retrieve all entities.

        Returns:
            List of serialised response DTOs.
        """
        models = await self.repository.get_all()
        return self.convert_list_to_response(models)

    async def get_by_id(self, id: int) -> ResponseDTO:
        """Retrieve a single entity by primary key.

        Args:
            id: Entity primary key.

        Returns:
            Serialised response DTO.

        Raises:
            HTTPException: 404 when the entity does not exist.
        """
        model = await self._get_or_404(id)
        return self.convert_to_response(model)

    async def put(self, id: int, data: CreateDTO) -> ResponseDTO:
        """Replace all mutable fields of an entity (PUT semantics).

        Args:
            id: Entity primary key.
            data: Complete replacement payload.

        Returns:
            Serialised updated entity.

        Raises:
            HTTPException: 404 when the entity does not exist.
        """
        model = await self._get_or_404(id)

        for field, value in data.model_dump().items():
            setattr(model, field, value)

        updated = await self.repository.save(model)
        return self.convert_to_response(updated)

    async def patch(self, id: int, data: PatchDTO) -> ResponseDTO:
        """Partially update an entity (PATCH semantics).

        Only fields explicitly included in the payload are updated.

        Args:
            id: Entity primary key.
            data: Partial update payload.

        Returns:
            Serialised updated entity.

        Raises:
            HTTPException: 404 when the entity does not exist.
        """
        model = await self._get_or_404(id)

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(model, field, value)

        updated = await self.repository.save(model)
        return self.convert_to_response(updated)

    async def delete(self, id: int) -> bool:
        """Soft-delete an entity.

        Args:
            id: Entity primary key.

        Returns:
            True when the operation succeeds.

        Raises:
            HTTPException: 404 when the entity does not exist.
        """
        model = await self._get_or_404(id)
        return await self.repository.soft_delete(model)

    # ------------------------------------------------------------------
    # Conversion helpers
    # ------------------------------------------------------------------

    def convert_to_orm(self, data: CreateDTO) -> ModelT:
        """Convert a creation DTO into an ORM model instance.

        Args:
            data: Input DTO.

        Returns:
            Unsaved ORM model instance.
        """
        return self.model(**data.model_dump())

    def convert_to_response(self, data: ModelT) -> ResponseDTO:
        """Serialise an ORM instance into a response DTO.

        Args:
            data: ORM entity instance.

        Returns:
            Validated response DTO.
        """
        return self.response_model.model_validate(data)

    def convert_list_to_response(self, data: list[ModelT]) -> list[ResponseDTO]:
        """Serialise a list of ORM instances into response DTOs.

        Args:
            data: List of ORM entity instances.

        Returns:
            List of validated response DTOs.
        """
        return [self.convert_to_response(item) for item in data]

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    async def _get_or_404(self, id: int) -> ModelT:
        """Fetch an entity or raise a 404 HTTPException.

        Centralizes the repetitive "get → check → raise" pattern so
        every public method stays clean.

        Args:
            id: Entity primary key.

        Returns:
            ORM entity instance.

        Raises:
            HTTPException: 404 when the entity does not exist.
        """
        model = await self.repository.get_by_id(id)
        if model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resource with id {id} not found",
            )
        return model


class UserCrudService(
    BaseCrudService[
        User,
        UserCreate,
        UserPatch,
        UserResponse,
    ]
):
    """CRUD service for the User entity.

    Inherits all standard CRUD operations from BaseCrudService.
    Add user-specific business logic as extra methods here.
    """

    def __init__(self, repository: RepositoryCrudInterface[User]) -> None:
        """Initialize the user service.

        Args:
            repository: User repository implementation.
        """
        super().__init__(
            repository=repository,
            model=User,
            response_model=UserResponse,
        )
