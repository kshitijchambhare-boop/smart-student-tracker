"""
test_tracker.py
Basic unit tests for the Smart Student Progress Tracker.
Run with: python -m pytest tests/
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.database import reset_db
from src import student, analytics


@pytest.fixture(autouse=True)
def clean_db():
    """Reset the database before every test for isolation."""
    reset_db()
    yield


def test_add_and_get_student():
    student.add_student("Alice Johnson", "R001", "Grade 10")
    s = student.get_student_by_roll("R001")
    assert s is not None
    assert s["name"] == "Alice Johnson"


def test_duplicate_roll_number_fails():
    student.add_student("Alice Johnson", "R001", "Grade 10")
    with pytest.raises(Exception):
        student.add_student("Bob Smith", "R001", "Grade 10")


def test_add_score_and_average():
    student.add_student("Alice Johnson", "R001", "Grade 10")
    student.add_score("R001", "Math", 80, 100, "2026-01-01")
    student.add_score("R001", "Math", 90, 100, "2026-02-01")
    avg = analytics.subject_average("R001", "Math")
    assert avg == 85.0


def test_score_for_unknown_student_raises():
    with pytest.raises(ValueError):
        student.add_score("NOPE", "Math", 80, 100, "2026-01-01")


def test_performance_trend_improving():
    student.add_student("Carlos Diaz", "R002", "Grade 9")
    student.add_score("R002", "Science", 50, 100, "2026-01-01")
    student.add_score("R002", "Science", 65, 100, "2026-02-01")
    student.add_score("R002", "Science", 80, 100, "2026-03-01")
    assert analytics.performance_trend("R002", "Science") == "improving"


def test_performance_trend_declining():
    student.add_student("Dana Lee", "R003", "Grade 9")
    student.add_score("R003", "Science", 90, 100, "2026-01-01")
    student.add_score("R003", "Science", 70, 100, "2026-02-01")
    student.add_score("R003", "Science", 50, 100, "2026-03-01")
    assert analytics.performance_trend("R003", "Science") == "declining"


def test_predict_next_score_not_enough_data():
    student.add_student("Eve Park", "R004", "Grade 9")
    student.add_score("R004", "Math", 80, 100, "2026-01-01")
    assert analytics.predict_next_score("R004", "Math") is None


def test_attendance_rate():
    student.add_student("Frank Wu", "R005", "Grade 9")
    student.mark_attendance("R005", "2026-01-01", True)
    student.mark_attendance("R005", "2026-01-02", True)
    student.mark_attendance("R005", "2026-01-03", False)
    rate = analytics.attendance_rate("R005")
    assert round(rate, 2) == 66.67


def test_needs_attention_flags_low_average():
    student.add_student("Grace Kim", "R006", "Grade 9")
    student.add_score("R006", "Math", 30, 100, "2026-01-01")
    student.add_score("R006", "Math", 35, 100, "2026-02-01")
    result = analytics.needs_attention("R006")
    assert result["flagged"] is True


def test_delete_student():
    student.add_student("Henry Ford", "R007", "Grade 9")
    assert student.delete_student("R007") is True
    assert student.get_student_by_roll("R007") is None
