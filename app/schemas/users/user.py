from typing import Annotated, Optional

from pydantic import BaseModel, StringConstraints, EmailStr

from app.enums import UserRole


class User(BaseModel):
    """
    Pydantic model representing a user entity.

    This model validates input data for user creation and updates,
    ensuring constraints on format, length, and required fields.
    """

    # Use EmailStr for robust email validation instead of a custom regex
    email: EmailStr

    # Optional field: just in case the user wants to change their email,
    # Or they want to recover their account and has no access to their old email
    recovery_email: Optional[EmailStr] = None

    # Do not allow empty strings for name and last_name,
    # And set reasonable length constraints
    name: Annotated[str, StringConstraints(min_length=2, max_length=60)]

    last_name: Annotated[str, StringConstraints(min_length=2, max_length=60)]

    # Password should enforce minimum security constraints
    password: Annotated[str, StringConstraints(min_length=8, max_length=255)]

    # Role is assumed to be an Enum, so we can directly use the UserRole type
    role: UserRole
