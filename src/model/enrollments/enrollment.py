from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class Enrollment(Base):
    """
    Enrollment model representing an enrollment in a cohort.

    The enrollment model has the main idea of linking a user to a cohort.
    Each component has a main language focused on the resources,
    then the component has 4 levels, and then each level has 1 cohort,
    and then each cohort has many enrollments, and each enrollment links a user to a cohort.

    Each cohort must have at least one user of type professor.

    """

    __tablename__ = "enrollments"

    # Foreign keys to link the enrollment to a user and a cohort
    # These are the columns that will contain the foreign keys.
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), primary_key=True)
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.course_id"), primary_key=True
    )

    enrollment_date: Mapped[datetime] = mapped_column(default=func.now())

    # Relationships to link the enrollment to a user and a cohort
    # This is not a new column, it's just a relationship to access the related user and cohort objects' data easily.
    course: Mapped["Course"] = relationship(back_populates="enrollments")
    user: Mapped["User"] = relationship(back_populates="enrollments")
