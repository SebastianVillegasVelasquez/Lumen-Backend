import pytest
from app.schemas.levels.level import Level, LevelCreate, LevelUpdate
from app.enums import EnglishLevel


class TestLevel:
    def test_level_create_valid(self, level_data):
        level = LevelCreate(**level_data)
        assert level.level_name == level_data["level_name"]

    def test_level_create_invalid_level_name(self):
        with pytest.raises(ValueError):
            LevelCreate(level_name="INVALID")

    def test_level_update(self, level_data):
        update_data = {"level_name": EnglishLevel.B1}
        level_update = LevelUpdate(**update_data)
        assert level_update.level_name == EnglishLevel.B1

    def test_level_from_attributes(self, level_data):
        level_data["level_id"] = 1
        level = Level(**level_data)
        assert level.level_id == 1
        assert level.level_name == level_data["level_name"]
