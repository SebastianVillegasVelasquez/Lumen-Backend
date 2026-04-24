from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.enums import EnglishLevel


class Level(Base):
    """
    Level model representing a level in the system.
    This means the English level of the cohort, for example, A1, A2, B1, B2.

    """
    __tablename__ = "levels"

    level_id: Mapped[int] = mapped_column(primary_key=True)

    level_name: Mapped[EnglishLevel] = mapped_column(
        SQLEnum(EnglishLevel, native_enum=False)
    )

    # Relationship with Cohort model
    cohorts: Mapped[list["Cohort"]] = relationship("cohorts", back_populates="level")
