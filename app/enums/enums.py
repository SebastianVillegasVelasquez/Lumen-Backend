from enum import Enum


class UserRole(Enum):
    SUPER_ADMIN = 0
    ADMIN = 1
    STUDENT = 2
    PROFESSOR = 3


class EnglishLevel(Enum):
    A1 = 0
    A2 = 1
    B1 = 2
    B2 = 3


class Language(Enum):
    ENGLISH = 0
    SPANISH = 1
