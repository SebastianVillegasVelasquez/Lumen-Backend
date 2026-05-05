from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base
from src.enums import UserRole


class User(Base):
    """
    UserCreate model representing a user in the system.
    It includes fields for email, password, and role.
    It may include additional fields as needed.
    Do not add fields that are not required.
    """

    # This is the name of the table in the database that this model will be mapped to.

    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True)
    recovery_email: Mapped[str] = mapped_column(unique=True, nullable=True)
    password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole, native_enum=False))
    is_active: Mapped[bool] = mapped_column(default=True)

    # Relationships
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="user")
    authored_courses: Mapped[list["Course"]] = relationship(back_populates="instructor")
    progress: Mapped[list["Progress"]] = relationship(back_populates="user")
