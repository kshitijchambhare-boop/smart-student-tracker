"""
student.py
CRUD operations for students, their exam scores, and attendance records.
"""

from src.database import get_connection


def add_student(name, roll_number, grade_level=""):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO students (name, roll_number, grade_level) VALUES (?, ?, ?)",
            (name, roll_number, grade_level),
        )
        conn.commit()
        return cur.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def get_all_students():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM students ORDER BY name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_student_by_roll(roll_number):
    conn = get_connection()
    row = conn.execute("SELECT * FROM students WHERE roll_number = ?", (roll_number,)).fetchone()
    conn.close()
    return dict(row) if row else None


def delete_student(roll_number):
    conn = get_connection()
    student = get_student_by_roll(roll_number)
    if not student:
        conn.close()
        return False
    conn.execute("DELETE FROM students WHERE id = ?", (student["id"],))
    conn.commit()
    conn.close()
    return True


def add_score(roll_number, subject, score, max_score, exam_date):
    student = get_student_by_roll(roll_number)
    if not student:
        raise ValueError(f"No student found with roll number '{roll_number}'")
    conn = get_connection()
    conn.execute(
        "INSERT INTO scores (student_id, subject, score, max_score, exam_date) VALUES (?, ?, ?, ?, ?)",
        (student["id"], subject, score, max_score, exam_date),
    )
    conn.commit()
    conn.close()


def get_scores(roll_number):
    student = get_student_by_roll(roll_number)
    if not student:
        return []
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM scores WHERE student_id = ? ORDER BY exam_date", (student["id"],)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_attendance(roll_number, date, present):
    student = get_student_by_roll(roll_number)
    if not student:
        raise ValueError(f"No student found with roll number '{roll_number}'")
    conn = get_connection()
    conn.execute(
        "INSERT INTO attendance (student_id, date, present) VALUES (?, ?, ?)",
        (student["id"], date, 1 if present else 0),
    )
    conn.commit()
    conn.close()


def get_attendance(roll_number):
    student = get_student_by_roll(roll_number)
    if not student:
        return []
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM attendance WHERE student_id = ? ORDER BY date", (student["id"],)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
