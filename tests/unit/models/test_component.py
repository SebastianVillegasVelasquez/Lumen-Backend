import pytest
from app.schemas.components.component import Component, ComponentCreate, ComponentUpdate
from app.enums import Language


class TestComponent:
    def test_component_create_valid(self, component_data):
        component = ComponentCreate(**component_data)
        assert component.component_name == component_data["component_name"]
        assert component.language == component_data["language"]

    def test_component_create_invalid_language(self):
        with pytest.raises(ValueError):
            ComponentCreate(component_name="Test Component", language="INVALID")

    def test_component_update(self, component_data):
        update_data = {"component_name": "Updated Component"}
        component_update = ComponentUpdate(**update_data)
        assert component_update.component_name == "Updated Component"
        assert component_update.language is None

    def test_component_from_attributes(self, component_data):
        component_data["component_id"] = 1
        component = Component(**component_data)
        assert component.component_id == 1
        assert component.component_name == component_data["component_name"]
