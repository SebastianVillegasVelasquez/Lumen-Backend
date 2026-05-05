from pydantic import BaseModel, ConfigDict


class EnrollmentBase(BaseModel):
    user_id: int
    cohort_id: int
    is_active: bool = True


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(BaseModel):
    is_active: bool | None = None


class Enrollment(EnrollmentBase):
    model_config = ConfigDict(from_attributes=True)
