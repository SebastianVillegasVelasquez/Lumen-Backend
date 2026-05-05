from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class Lesson(Base):

    __tablename__ = "lessons"

    lesson_id: Mapped[int] = mapped_column(primary_key=True)
    lesson_name: Mapped[str]

    # Foreign Key relationship
    section_id: Mapped[int] = mapped_column(
        ForeignKey("sections.section_id"), nullable=False
    )

    # relationships
    section: Mapped["Section"] = relationship(back_populates="lessons")
    progress: Mapped[list["Progress"]] = relationship(back_populates="lesson")
