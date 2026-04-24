from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base



class Enrollment(Base):
    """
    Enrollment model representing an enrollment in a cohort.

    The enrollment model has the main idea of linking a user to a cohort.
    Each component has a main language focused on the resources,
    then the component has 4 levels, and then each level has 1 cohort,
    and then each cohort has many enrollments, and each enrollment links a user to a cohort.

    Each cohort must have at least one user of type professor.

    """

    from app.models import Cohort, User
    __tablename__ = "enrollments"

    # enrollment_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Foreign keys to link the enrollment to a user and a cohort
    # These are the columns that will contain the foreign keys.
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    cohort_id: Mapped[int] = mapped_column(ForeignKey("cohorts.cohort_id"), primary_key=True)

    is_active: Mapped[bool] = mapped_column(default=True)

    # Relationships to link the enrollment to a user and a cohort
    # This is not a new column, it's just a relationship to access the related user and cohort objects' data easily.
    cohort: Mapped["Cohort"] = relationship(back_populates="enrollments")
    user: Mapped["User"] = relationship(back_populates="enrollments")
