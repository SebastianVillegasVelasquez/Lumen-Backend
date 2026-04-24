from app.db import Base
from app.enums import Language
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLEnum


class Component(Base):
    """
    This class represents a component model in the system.

    Each component has a main language focused on the resources,
    do not add languages that are not used in the resources.

    """

    __tablename__ = "components"

    component_id: Mapped[int] = mapped_column(primary_key=True)
    component_name: Mapped[str]

    language: Mapped[Language] = mapped_column(SQLEnum(Language, native_enum=False))
