from pydantic import BaseModel, ConfigDict
from app.enums import Language


class ComponentBase(BaseModel):
    component_name: str
    language: Language


class ComponentCreate(ComponentBase):
    pass


class ComponentUpdate(BaseModel):
    component_name: str | None = None
    language: Language | None = None


class Component(ComponentBase):
    component_id: int

    model_config = ConfigDict(from_attributes=True)
