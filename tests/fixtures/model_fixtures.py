"""Non-generic pytest fixtures for model testing.

Imports from generic module are re-exported for backward compatibility.
"""

from tests.fixtures.generic import BaseCrudServiceTests, FakeBaseRepository

__all__ = [
    "BaseCrudServiceTests",
    "FakeBaseRepository",
]
