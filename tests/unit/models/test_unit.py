import pytest
from app.schemas.unit.unit import Unit, UnitCreate, UnitUpdate


class TestUnit:
    def test_unit_create_valid(self, unit_data):
        unit = UnitCreate(**unit_data)
        assert unit.title == unit_data["title"]
        assert unit.description == unit_data["description"]
        assert unit.scorm_url == unit_data["scorm_url"]
        assert unit.level_id == unit_data["level_id"]

    def test_unit_create_invalid_missing_field(self):
        with pytest.raises(ValueError):
            UnitCreate(title="Test Unit", scorm_url="http://example.com")  # missing level_id

    def test_unit_update(self, unit_data):
        update_data = {"title": "Updated Unit"}
        unit_update = UnitUpdate(**update_data)
        assert unit_update.title == "Updated Unit"
        assert unit_update.description is None

    def test_unit_from_attributes(self, unit_data):
        unit_data["unit_id"] = 1
        unit = Unit(**unit_data)
        assert unit.unit_id == 1
        assert unit.title == unit_data["title"]
