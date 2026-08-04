"""
visualizer.py
Generates matplotlib charts for student progress: score-over-time line
charts and class-wide comparison bar charts. Charts are saved as PNG
files into the reports/ directory.
"""

import os
import matplotlib
matplotlib.use("Agg")  # headless backend, no display needed
import matplotlib.pyplot as plt

from src.student import get_scores

REPORTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports"
)


def _ensure_reports_dir():
    os.makedirs(REPORTS_DIR, exist_ok=True)


def plot_student_progress(roll_number, student_name):
    """Line chart of a single student's percentage scores over time."""
    scores = get_scores(roll_number)
    if not scores:
        return None

    scores = sorted(scores, key=lambda s: s["exam_date"])
    dates = [s["exam_date"] for s in scores]
    percentages = [s["score"] / s["max_score"] * 100 for s in scores]
    subjects = [s["subject"] for s in scores]

    _ensure_reports_dir()
    plt.figure(figsize=(8, 5))
    plt.plot(dates, percentages, marker="o", linewidth=2, color="#4C72B0")
    for i, subj in enumerate(subjects):
        plt.annotate(subj, (dates[i], percentages[i]), textcoords="offset points",
                     xytext=(0, 8), fontsize=8, ha="center")

    plt.title(f"Progress Over Time — {student_name} ({roll_number})")
    plt.xlabel("Exam Date")
    plt.ylabel("Score (%)")
    plt.ylim(0, 105)
    plt.xticks(rotation=45, ha="right")
    plt.grid(alpha=0.3)
    plt.tight_layout()

    filepath = os.path.join(REPORTS_DIR, f"{roll_number}_progress.png")
    plt.savefig(filepath, dpi=150)
    plt.close()
    return filepath


def plot_class_comparison(class_summary_data):
    """Bar chart comparing average scores across all students in a class."""
    data = [d for d in class_summary_data if d["average"] is not None]
    if not data:
        return None

    names = [d["name"] for d in data]
    averages = [d["average"] for d in data]
    colors = ["#C44E52" if d["attention"]["flagged"] else "#55A868" for d in data]

    _ensure_reports_dir()
    plt.figure(figsize=(max(6, len(names) * 1.2), 5))
    plt.bar(names, averages, color=colors)
    plt.axhline(50, color="gray", linestyle="--", linewidth=1, label="Pass threshold (50%)")
    plt.title("Class Average Comparison")
    plt.xlabel("Student")
    plt.ylabel("Average Score (%)")
    plt.ylim(0, 105)
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()

    filepath = os.path.join(REPORTS_DIR, "class_comparison.png")
    plt.savefig(filepath, dpi=150)
    plt.close()
    return filepath
