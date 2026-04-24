import pytest
from app.schemas.scorm_progress.scorm_progress import ScormProgress, ScormProgressCreate, ScormProgressUpdate


class TestScormProgress:
    def test_scorm_progress_create_valid(self, scorm_progress_data):
        progress = ScormProgressCreate(**scorm_progress_data)
        assert progress.user_id == scorm_progress_data["user_id"]
        assert progress.unit_id == scorm_progress_data["unit_id"]
        assert progress.score == scorm_progress_data["score"]
        assert progress.status == scorm_progress_data["status"]

    def test_scorm_progress_create_invalid_missing_field(self):
        with pytest.raises(ValueError):
            ScormProgressCreate(user_id=1)  # missing unit_id

    def test_scorm_progress_update(self, scorm_progress_data):
        update_data = {"score": 85.5, "status": "completed"}
        progress_update = ScormProgressUpdate(**update_data)
        assert progress_update.score == 85.5
        assert progress_update.status == "completed"

    def test_scorm_progress_from_attributes(self, scorm_progress_data):
        scorm_progress_data["id"] = 1
        progress = ScormProgress(**scorm_progress_data)
        assert progress.id == 1
        assert progress.user_id == scorm_progress_data["user_id"]
