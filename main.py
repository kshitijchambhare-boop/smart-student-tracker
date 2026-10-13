"""
Smart Student Progress Tracker
--------------------------------
A CLI application to track student exam scores and attendance,
then use simple analytics to detect trends, predict future
performance, and flag students who may need extra support.

Run: python main.py
"""

from src.database import initialize_db
from src import student, analytics, visualizer


def menu():
    print("""
==========================================
   SMART STUDENT PROGRESS TRACKER
==========================================
 1. Add student
 2. Add exam score
 3. Mark attendance
 4. View student report
 5. View class summary
 6. Generate progress chart (single student)
 7. Generate class comparison chart
 8. List all students
 9. Delete student
 10. Evaluate prediction error
 0. Exit
==========================================
""")


def add_student_flow():
    name = input("Student name: ").strip()
    roll = input("Roll number (unique ID): ").strip()
    grade = input("Grade/class level (optional): ").strip()
    try:
        student.add_student(name, roll, grade)
        print(f"✔ Added student '{name}' ({roll})")
    except Exception as e:
        print(f"✘ Error: {e}")


def add_score_flow():
    roll = input("Student roll number: ").strip()
    subject = input("Subject: ").strip()
    score = float(input("Score obtained: ").strip())
    max_score = float(input("Max score (default 100): ").strip() or 100)
    date = input("Exam date (YYYY-MM-DD): ").strip()
    try:
        student.add_score(roll, subject, score, max_score, date)
        print("✔ Score recorded")
    except Exception as e:
        print(f"✘ Error: {e}")


def mark_attendance_flow():
    roll = input("Student roll number: ").strip()
    date = input("Date (YYYY-MM-DD): ").strip()
    present = input("Present? (y/n): ").strip().lower() == "y"
    try:
        student.mark_attendance(roll, date, present)
        print("✔ Attendance recorded")
    except Exception as e:
        print(f"✘ Error: {e}")


def view_report_flow():
    roll = input("Student roll number: ").strip()
    s = student.get_student_by_roll(roll)
    if not s:
        print("✘ Student not found")
        return

    avg = analytics.overall_average(roll)
    att = analytics.attendance_rate(roll)
    trend = analytics.performance_trend(roll)
    prediction = analytics.predict_next_score(roll)
    attention = analytics.needs_attention(roll)

    print(f"\n--- Report for {s['name']} ({roll}) ---")
    print(f"Overall average : {avg if avg is not None else 'N/A'}%")
    print(f"Attendance rate : {att if att is not None else 'N/A'}%")
    print(f"Trend           : {trend or 'N/A (need 2+ scores)'}")
    print(f"Predicted next  : {prediction if prediction is not None else 'N/A'}%")
    if attention["flagged"]:
        print(f"⚠ NEEDS ATTENTION: {', '.join(attention['reasons'])}")
    else:
        print("✔ No concerns flagged")
    print()


def view_class_summary_flow():
    students = student.get_all_students()
    if not students:
        print("No students yet.")
        return
    summary = analytics.class_summary(students)
    print(f"\n{'Name':<20}{'Avg%':<8}{'Attend%':<10}{'Trend':<12}{'Predicted':<10}{'Flag'}")
    print("-" * 70)
    for s in summary:
        flag = "⚠" if s["attention"]["flagged"] else ""
        print(f"{s['name']:<20}{str(s['average']):<8}{str(s['attendance']):<10}"
              f"{str(s['trend']):<12}{str(s['predicted_next']):<10}{flag}")
    print()


def chart_flow():
    roll = input("Student roll number: ").strip()
    s = student.get_student_by_roll(roll)
    if not s:
        print("✘ Student not found")
        return
    path = visualizer.plot_student_progress(roll, s["name"])
    print(f"✔ Chart saved to: {path}" if path else "✘ No score data to chart")


def class_chart_flow():
    students = student.get_all_students()
    if not students:
        print("No students yet.")
        return
    summary = analytics.class_summary(students)
    path = visualizer.plot_class_comparison(summary)
    print(f"✔ Chart saved to: {path}" if path else "✘ No score data to chart")


def list_students_flow():
    students = student.get_all_students()
    if not students:
        print("No students yet.")
        return
    for s in students:
        print(f"  {s['roll_number']:<10} {s['name']:<20} {s['grade_level']}")


def delete_student_flow():
    roll = input("Roll number to delete: ").strip()
    if student.delete_student(roll):
        print("✔ Deleted")
    else:
        print("✘ Student not found")


def prediction_error_flow():
    """Display historical prediction MAE for one student and subject."""
    roll = input("Student roll number: ").strip()

    s = student.get_student_by_roll(roll)
    if not s:
        print("Student not found.")
        return

    subject = input("Subject to evaluate: ").strip()
    if not subject:
        print("Subject cannot be empty.")
        return

    mae = analytics.evaluate_prediction_error(roll, subject)

    if mae is None:
        print("Not enough exam data (need at least 3 scores for this subject).")
    else:
        print(f"Prediction MAE for {s['name']} in {subject}: "
              f"{mae:.2f} percentage points")


def main():
    initialize_db()
    actions = {
        "1": add_student_flow,
        "2": add_score_flow,
        "3": mark_attendance_flow,
        "4": view_report_flow,
        "5": view_class_summary_flow,
        "6": chart_flow,
        "7": class_chart_flow,
        "8": list_students_flow,
        "9": delete_student_flow,
        "10": prediction_error_flow,
    }
    while True:
        menu()
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            try:
                action()
            except Exception as e:
                print(f"✘ Unexpected error: {e}")
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
