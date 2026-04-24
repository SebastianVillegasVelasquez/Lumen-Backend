from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Cohort(Base):
    """
    This class represents a cohort model in the system.

    It is not an enrollment model, but a relationship between a level and a component.
    It is a one-to-one relationship between levels and components.
    """
    __tablename__ = "cohorts"

    cohort_id: Mapped[int] = mapped_column(
        ForeignKey("levels.level_id"),
        primary_key=True
    )
    cohort_name: Mapped[str] = mapped_column(String(200))

    component_id: Mapped[int] = mapped_column(ForeignKey("components.component_id"))
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.level_id"))

    component: Mapped["Component"] = relationship(back_populates="cohorts")
    level: Mapped["Level"] = relationship(back_populates="cohorts")
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="cohorts")
