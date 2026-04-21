from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    This class is the base class for all models that gonna be mapped to the database.
    If it is necessary to add a field in all models, it should be added here.
    Do not create another base class for models.
    Please avoid multiple inheritance.

    """

    # This avoids creating a table for this class.
    __abstract__ = True

    # These fields will be added to all models to keep track of the creation and update times.
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
