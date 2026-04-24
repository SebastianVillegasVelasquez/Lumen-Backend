from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.enums import UserRole
from app.db.base import Base
from sqlalchemy import Enum as SQLEnum


class User(Base):
    """
    User model representing a user in the system.
    It includes fields for email, password, and role.
    It may include additional fields as needed.
    Do not add fields that are not required.
    """

    # This is the name of the table in the database that this model will be mapped to.

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True)
    recovery_email: Mapped[str] = mapped_column(unique=True, nullable=True)
    password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole, native_enum=False))

    scorm_progress: Mapped[list["ScormProgress"]] = relationship(back_populates="user")
