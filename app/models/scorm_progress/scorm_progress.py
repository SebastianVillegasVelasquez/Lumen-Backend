from sqlalchemy import ForeignKey, Text, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.db import Base


class ScormProgress(Base):
    """
    ScormProgress model representing the tracking data for a user's interaction 
    with a specific SCORM learning unit.

    This model stores data sent by the SCORM API (Run-Time Service), allowing 
    the system to track grades, completion status, and session state (suspend data) 
    so students can resume their progress.
    """

    __tablename__ = "scorm_progress"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Foreign keys to link progress to a specific user and a specific unit
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.unit_id"), nullable=False)

    # SCORM Core Data: Mapping standard CMI elements
    # score: represents 'cmi.core.score.raw'
    score: Mapped[float] = mapped_column(Float, default=0.0)

    # status: represents 'cmi.core.lesson_status' (e.g., passed, completed, failed, incomplete)
    status: Mapped[str] = mapped_column(String(20), default="not attempted")

    # total_time: represents 'cmi.core.total_time'
    total_time: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # suspend_data: represents 'cmi.suspend_data'. 
    # Stored as Text to allow the SCORM package to save its internal state/variables.
    suspend_data: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    # Enables access to user data from a progress record (e.g., progress.user.name)
    user: Mapped["User"] = relationship(back_populates="scorm_progress")

    # Enables access to unit metadata (e.g., progress.unit.title)
    unit: Mapped["Unit"] = relationship(back_populates="progress_records")