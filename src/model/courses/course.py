from sqlalchemy import JSON, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class Course(Base):

    __tablename__ = "courses"

    course_id: Mapped[int] = mapped_column(primary_key=True)
    course_name: Mapped[str]
    course_description: Mapped[str] = mapped_column(String(2000))
    course_price: Mapped[float] = mapped_column(default=0.0)
    course_duration: Mapped[int] = mapped_column(default=0)
    course_tags: Mapped[list[str]] = mapped_column(JSON, default=list)

    # Foreign Key
    instructor_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), nullable=False
    )

    # Relationships
    instructor: Mapped["User"] = relationship(back_populates="authored_courses")
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="course")
    modules: Mapped[list["Module"]] = relationship(back_populates="course")
    progress: Mapped[list["Progress"]] = relationship(back_populates="course")
