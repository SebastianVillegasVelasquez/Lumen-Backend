import pytest
from app.schemas.enrollments.enrollment import Enrollment, EnrollmentCreate, EnrollmentUpdate


class TestEnrollment:
    def test_enrollment_create_valid(self, enrollment_data):
        enrollment = EnrollmentCreate(**enrollment_data)
        assert enrollment.user_id == enrollment_data["user_id"]
        assert enrollment.cohort_id == enrollment_data["cohort_id"]
        assert enrollment.is_active == enrollment_data["is_active"]

    def test_enrollment_create_invalid_missing_field(self):
        with pytest.raises(ValueError):
            EnrollmentCreate(user_id=1)  # missing cohort_id

    def test_enrollment_update(self, enrollment_data):
        update_data = {"is_active": False}
        enrollment_update = EnrollmentUpdate(**update_data)
        assert enrollment_update.is_active is False

    def test_enrollment_from_attributes(self, enrollment_data):
        enrollment = Enrollment(**enrollment_data)
        assert enrollment.user_id == enrollment_data["user_id"]
        assert enrollment.cohort_id == enrollment_data["cohort_id"]
