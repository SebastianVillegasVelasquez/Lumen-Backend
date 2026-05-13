"""Generic (reusable across all models) test fixtures and base classes.

This module contains:
- FakeBaseRepository: Generic in-memory repository for testing
- BaseCrudServiceTests: Generic CRUD test contract that all model-specific tests inherit from
"""

from tests.fixtures.generic.base_crud_service_tests import BaseCrudServiceTests
from tests.fixtures.generic.fake_base_repository import FakeBaseRepository

__all__ = [
    "BaseCrudServiceTests",
    "FakeBaseRepository",
]
