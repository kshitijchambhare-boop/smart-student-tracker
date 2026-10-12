# 🎓 Smart Student Progress Tracker

A Python-based education tool that tracks student exam scores and attendance,
then applies simple data analytics to **detect performance trends, predict
future scores, and automatically flag students who may need extra support.**

Built with SQLite, NumPy, and Matplotlib — no external services required.

## ✨ Features

- 👤 **Student management** — add, list, and remove students
- 📊 **Score tracking** — record exam scores per subject over time
- 📅 **Attendance tracking** — mark daily present/absent records
- 🧠 **Smart analytics**
  - Overall & subject-wise averages
  - Attendance rate
  - Trend detection (`improving` / `declining` / `stable`) via linear regression
  - Predicted next-exam score
  - Automatic "needs attention" flagging (low scores, poor attendance, or declining trend)
  - Historical prediction error evaluation using Mean Absolute Error (MAE)
- 📈 **Auto-generated charts** — per-student progress line charts and class-wide comparison bar charts
- ✅ **Tested** — unit test suite included (pytest)

## 📁 Project Structure

```
smart-student-tracker/
├── main.py                # CLI entry point
├── seed_demo_data.py       # Populates sample data to try the app instantly
├── requirements.txt
├── src/
│   ├── database.py         # SQLite schema & connection handling
│   ├── student.py          # CRUD for students, scores, attendance
│   ├── analytics.py        # Trend detection & prediction (the "smart" layer)
│   └── visualizer.py       # Matplotlib chart generation
├── tests/
│   └── test_tracker.py     # Unit tests
├── data/                   # SQLite database lives here (gitignored)
└── reports/                # Generated chart images (gitignored)
```

## 🚀 Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/smart-student-tracker.git
cd smart-student-tracker

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Seed sample data to explore the app immediately
python seed_demo_data.py

# 4. Run the app
python main.py
```

## 🖥️ Example CLI Session

```
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
Choose an option: 4
Student roll number: S003

--- Report for Rohan Mehta (S003) ---
Overall average : 57.0%
Attendance rate : 42.86%
Trend           : declining
Predicted next  : 35.7%
⚠ NEEDS ATTENTION: Low attendance (42.86%), Declining performance trend
```

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

## 🛠️ How the "Smart" Prediction Works

Each student's percentage scores are plotted against exam order and fit
with a simple linear regression (`numpy.polyfit`). The slope of that line
determines the trend label, and extrapolating one step forward gives the
predicted next score. It's intentionally lightweight — easy to read, easy
to extend (e.g. swap in `scikit-learn` for a more advanced model) — while
still giving teachers a genuinely useful early-warning signal.

## Prediction Error Evaluation

This feature evaluates the accuracy of student score predictions using Mean Absolute Error (MAE).

### How It Works

- Requires at least 3 exam scores for a selected subject.
- Uses rolling linear regression to predict each exam from previous scores.
- Converts scores to percentages and limits predictions to 0–100%.
- Calculates MAE in percentage points. Lower MAE means smaller historical prediction errors.

### Usage

Run:

    python main.py

Select option `10. Evaluate prediction error`, then enter the student's roll number and subject.

Example:

    Student roll number: S01
    Subject to evaluate: Math
    Prediction MAE for Test in Math: 2.00 percentage points

MAE measures historical prediction error and does not guarantee future accuracy.

### Testing

Run all unit tests:

    python -m pytest tests/ -v

Seven new unit tests cover the prediction error evaluation feature.

## 🗺️ Ideas for Extending This Project

- Add a Flask/FastAPI web dashboard on top of the existing `src/` logic
- Export PDF report cards per student
- Add email/SMS alerts for flagged students
- Support multiple classes/teachers with authentication
- Swap linear regression for a proper ML model (e.g. `scikit-learn`)

## 📄 License

MIT — see [LICENSE](LICENSE).
