from enum import Enum


class UserRole(Enum):
    SUPER_ADMIN = 0
    ADMIN = 1
    STUDENT = 2
    PROFESSOR = 3


class ProgressStatus(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    COMPLETED = 2
