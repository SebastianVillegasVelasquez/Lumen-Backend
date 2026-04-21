from enum import Enum


class UserRole(Enum):
    SUPER_ADMIN = 0
    ADMIN = 1
    STUDENT = 2
    PROFESSOR = 3
