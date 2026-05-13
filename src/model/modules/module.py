from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.db import Base

if TYPE_CHECKING:
    from src.model.courses.course import Course
    from src.model.sections.section import Section


class Module(Base):
    __tablename__ = "modules"

    module_id: Mapped[int] = mapped_column(primary_key=True)
    module_name: Mapped[str]
    module_description: Mapped[str]

    # Foreign Key relationship
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.course_id"), nullable=False
    )

    # Relationships
    course: Mapped[Course] = relationship(back_populates="modules")
    sections: Mapped[list[Section]] = relationship(back_populates="module")
