"""
seed_demo_data.py
Populates the database with realistic sample data so you can explore
the tracker's features immediately after cloning the repo.

Run: python seed_demo_data.py
"""

from src.database import reset_db
from src import student, analytics, visualizer

DEMO_STUDENTS = [
    ("Aarav Sharma", "S001", "Grade 10"),
    ("Priya Patel", "S002", "Grade 10"),
    ("Rohan Mehta", "S003", "Grade 10"),
    ("Sneha Rao", "S004", "Grade 10"),
]

# (roll, subject, score, max_score, date)
DEMO_SCORES = [
    ("S001", "Math", 55, 100, "2026-01-10"),
    ("S001", "Math", 62, 100, "2026-02-10"),
    ("S001", "Math", 74, 100, "2026-03-10"),
    ("S001", "Science", 60, 100, "2026-01-15"),
    ("S001", "Science", 66, 100, "2026-02-15"),

    ("S002", "Math", 92, 100, "2026-01-10"),
    ("S002", "Math", 89, 100, "2026-02-10"),
    ("S002", "Math", 95, 100, "2026-03-10"),
    ("S002", "Science", 88, 100, "2026-01-15"),
    ("S002", "Science", 91, 100, "2026-02-15"),

    ("S003", "Math", 70, 100, "2026-01-10"),
    ("S003", "Math", 58, 100, "2026-02-10"),
    ("S003", "Math", 42, 100, "2026-03-10"),
    ("S003", "Science", 65, 100, "2026-01-15"),
    ("S003", "Science", 50, 100, "2026-02-15"),

    ("S004", "Math", 80, 100, "2026-01-10"),
    ("S004", "Math", 82, 100, "2026-02-10"),
    ("S004", "Math", 79, 100, "2026-03-10"),
    ("S004", "Science", 85, 100, "2026-01-15"),
    ("S004", "Science", 83, 100, "2026-02-15"),
]

DEMO_ATTENDANCE = {
    "S001": [True, True, False, True, True, True, False],
    "S002": [True, True, True, True, True, True, True],
    "S003": [False, True, False, False, True, False, True],
    "S004": [True, True, True, False, True, True, True],
}


def run():
    reset_db()
    for name, roll, grade in DEMO_STUDENTS:
        student.add_student(name, roll, grade)

    for roll, subject, score, max_score, date in DEMO_SCORES:
        student.add_score(roll, subject, score, max_score, date)

    dates = [f"2026-01-{i+1:02d}" for i in range(7)]
    for roll, presents in DEMO_ATTENDANCE.items():
        for date, present in zip(dates, presents):
            student.mark_attendance(roll, date, present)

    print("✔ Demo data seeded successfully.\n")

    students = student.get_all_students()
    summary = analytics.class_summary(students)
    print(f"{'Name':<20}{'Avg%':<8}{'Attend%':<10}{'Trend':<12}{'Predicted':<10}{'Flag'}")
    print("-" * 70)
    for s in summary:
        flag = "⚠ NEEDS ATTENTION" if s["attention"]["flagged"] else ""
        print(f"{s['name']:<20}{str(s['average']):<8}{str(s['attendance']):<10}"
              f"{str(s['trend']):<12}{str(s['predicted_next']):<10}{flag}")

    print("\nGenerating charts...")
    for s in students:
        visualizer.plot_student_progress(s["roll_number"], s["name"])
    visualizer.plot_class_comparison(summary)
    print("✔ Charts saved in reports/")


if __name__ == "__main__":
    run()
