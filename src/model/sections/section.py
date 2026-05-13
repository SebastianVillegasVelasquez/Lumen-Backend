from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.db import Base

if TYPE_CHECKING:
    from src.model.modules.module import Module
    from src.model.lessons.lesson import Lesson


class Section(Base):
    __tablename__ = "sections"

    section_id: Mapped[int] = mapped_column(primary_key=True)
    section_name: Mapped[str]
    section_description: Mapped[str]
    section_order: Mapped[int]

    # Foreign Key relationship

    module_id: Mapped[int] = mapped_column(
        ForeignKey("modules.module_id"), nullable=False
    )

    # Relationships
    module: Mapped[Module] = relationship(back_populates="sections")
    lessons: Mapped[list[Lesson]] = relationship(back_populates="section")
