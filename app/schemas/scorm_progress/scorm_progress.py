from pydantic import BaseModel, ConfigDict
from typing import Optional


class ScormProgressBase(BaseModel):
    user_id: int
    unit_id: int
    score: float = 0.0
    status: str = "not attempted"
    total_time: Optional[str] = None
    suspend_data: Optional[str] = None


class ScormProgressCreate(ScormProgressBase):
    pass


class ScormProgressUpdate(BaseModel):
    score: float | None = None
    status: str | None = None
    total_time: str | None = None
    suspend_data: str | None = None


class ScormProgress(ScormProgressBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
