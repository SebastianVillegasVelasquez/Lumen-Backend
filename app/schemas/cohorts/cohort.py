from pydantic import BaseModel, ConfigDict


class CohortBase(BaseModel):
    cohort_name: str
    component_id: int
    level_id: int


class CohortCreate(CohortBase):
    pass


class CohortUpdate(BaseModel):
    cohort_name: str | None = None
    component_id: int | None = None
    level_id: int | None = None


class Cohort(CohortBase):
    cohort_id: int

    model_config = ConfigDict(from_attributes=True)
