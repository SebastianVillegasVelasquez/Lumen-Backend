import pytest
from app.schemas.cohorts.cohort import Cohort, CohortCreate, CohortUpdate


class TestCohort:
    def test_cohort_create_valid(self, cohort_data):
        cohort = CohortCreate(**cohort_data)
        assert cohort.cohort_name == cohort_data["cohort_name"]
        assert cohort.component_id == cohort_data["component_id"]
        assert cohort.level_id == cohort_data["level_id"]

    def test_cohort_create_invalid_missing_field(self):
        with pytest.raises(ValueError):
            CohortCreate(cohort_name="Test Cohort", component_id=1)  # missing level_id

    def test_cohort_update(self, cohort_data):
        update_data = {"cohort_name": "Updated Cohort"}
        cohort_update = CohortUpdate(**update_data)
        assert cohort_update.cohort_name == "Updated Cohort"
        assert cohort_update.component_id is None

    def test_cohort_from_attributes(self, cohort_data):
        cohort_data["cohort_id"] = 1
        cohort = Cohort(**cohort_data)
        assert cohort.cohort_id == 1
        assert cohort.cohort_name == cohort_data["cohort_name"]
