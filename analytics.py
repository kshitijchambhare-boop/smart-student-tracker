"""
analytics.py
The "smart" part of the tracker: computes averages, detects performance
trends, predicts likely next-exam performance using linear regression,
and flags students who may need attention.
"""

import numpy as np
from src.student import get_scores, get_attendance


def subject_average(roll_number, subject=None):
    """Average percentage score, optionally filtered to one subject."""
    scores = get_scores(roll_number)
    if subject:
        scores = [s for s in scores if s["subject"].lower() == subject.lower()]
    if not scores:
        return None
    percentages = [s["score"] / s["max_score"] * 100 for s in scores]
    return round(sum(percentages) / len(percentages), 2)


def overall_average(roll_number):
    return subject_average(roll_number)


def attendance_rate(roll_number):
    records = get_attendance(roll_number)
    if not records:
        return None
    present = sum(r["present"] for r in records)
    return round(present / len(records) * 100, 2)


def performance_trend(roll_number, subject=None):
    """
    Returns 'improving', 'declining', 'stable', or None (not enough data),
    based on the slope of a linear fit over percentage scores across time.
    """
    scores = get_scores(roll_number)
    if subject:
        scores = [s for s in scores if s["subject"].lower() == subject.lower()]
    if len(scores) < 2:
        return None

    scores = sorted(scores, key=lambda s: s["exam_date"])
    percentages = np.array([s["score"] / s["max_score"] * 100 for s in scores])
    x = np.arange(len(percentages))

    slope, _ = np.polyfit(x, percentages, 1)

    if slope > 1.5:
        return "improving"
    elif slope < -1.5:
        return "declining"
    else:
        return "stable"


def predict_next_score(roll_number, subject=None):
    """
    Predicts the next likely percentage score using a simple linear
    regression fit over past exam performance. Returns None if there
    isn't enough data (fewer than 2 data points).
    """
    scores = get_scores(roll_number)
    if subject:
        scores = [s for s in scores if s["subject"].lower() == subject.lower()]
    if len(scores) < 2:
        return None

    scores = sorted(scores, key=lambda s: s["exam_date"])
    percentages = np.array([s["score"] / s["max_score"] * 100 for s in scores])
    x = np.arange(len(percentages))

    slope, intercept = np.polyfit(x, percentages, 1)
    next_x = len(percentages)
    prediction = slope * next_x + intercept

    return round(float(np.clip(prediction, 0, 100)), 2)


def needs_attention(roll_number, score_threshold=50, attendance_threshold=75):
    """
    Flags a student as needing attention if their overall average is
    below score_threshold, attendance is below attendance_threshold,
    or their trend is declining.
    """
    reasons = []
    avg = overall_average(roll_number)
    att = attendance_rate(roll_number)
    trend = performance_trend(roll_number)

    if avg is not None and avg < score_threshold:
        reasons.append(f"Low overall average ({avg}%)")
    if att is not None and att < attendance_threshold:
        reasons.append(f"Low attendance ({att}%)")
    if trend == "declining":
        reasons.append("Declining performance trend")

    return {"flagged": len(reasons) > 0, "reasons": reasons}


def class_summary(students):
    """Build a summary list of stats for every student, for reporting."""
    summary = []
    for s in students:
        roll = s["roll_number"]
        summary.append({
            "name": s["name"],
            "roll_number": roll,
            "average": overall_average(roll),
            "attendance": attendance_rate(roll),
            "trend": performance_trend(roll),
            "predicted_next": predict_next_score(roll),
            "attention": needs_attention(roll),
        })
    return summary
