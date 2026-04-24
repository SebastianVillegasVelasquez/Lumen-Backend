from pydantic import BaseModel, ConfigDict
from typing import Optional


class UnitBase(BaseModel):
    title: str
    description: Optional[str] = None
    scorm_url: str
    level_id: int


class UnitCreate(UnitBase):
    pass


class UnitUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    scorm_url: str | None = None
    level_id: int | None = None


class Unit(UnitBase):
    unit_id: int

    model_config = ConfigDict(from_attributes=True)
