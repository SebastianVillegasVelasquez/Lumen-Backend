from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.db import Base
from src.enums.enums import ProgressStatus


class Progress(Base):

    __tablename__ = "progress"

    progress_id: Mapped[int] = mapped_column(primary_key=True)
    progress_percentage: Mapped[float] = mapped_column(default=0.0)
    progress_status: Mapped[ProgressStatus] = mapped_column(
        default=ProgressStatus.NOT_STARTED
    )

    # Foreign keys relationship
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.lesson_id"), nullable=False
    )
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.course_id"), nullable=False
    )

    # Relationships
    course: Mapped["Course"] = relationship(back_populates="progress")
    lesson: Mapped["Lesson"] = relationship(back_populates="progress")
    user: Mapped["User"] = relationship(back_populates="progress")
