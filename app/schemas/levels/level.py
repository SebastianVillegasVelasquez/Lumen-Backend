from pydantic import BaseModel, ConfigDict
from app.enums import EnglishLevel


class LevelBase(BaseModel):
    level_name: EnglishLevel


class LevelCreate(LevelBase):
    pass


class LevelUpdate(BaseModel):
    level_name: EnglishLevel | None = None


class Level(LevelBase):
    level_id: int

    model_config = ConfigDict(from_attributes=True)
