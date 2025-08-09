from flask import Flask, jsonify  # type: ignore
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("./src/hospital_database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Hospital API"})


@app.route("/api/patients", methods=["GET"])
def get_patients():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patient")
        patients = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(patients)
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route("/api/patients/doctor/<string:doctor_id>", methods=["GET"])
def get_patients_by_doctor(doctor_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.FirstName, p.LastName
            FROM patient p
            JOIN patient_doctor pd ON p.PatientID = pd.PatientID
            WHERE pd.DoctorID = ?
        """, (doctor_id,))
        patients = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(patients)
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route("/api/patients/exam-count", methods=["GET"])
def get_exam_counts():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.FirstName, p.LastName, COUNT(pe.ExamID) AS ExamCount
            FROM patient p
            LEFT JOIN patient_examination pe ON p.PatientID = pe.PatientID
            GROUP BY p.PatientID, p.FirstName, p.LastName
        """)
        counts = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(counts)
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route("/api/doctors/blood-test", methods=["GET"])
def get_blood_test_doctors():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT d.Title, d.FirstName, d.LastName
            FROM doctor d
            JOIN doctor_examination de ON d.DoctorID = de.DoctorID
            JOIN examination e ON de.ExamID = e.ExamID
            WHERE e.ExamType = 'Blood Test'
        """)
        doctors = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(doctors)
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route("/api/kpi/revenue", methods=["GET"])
def get_revenue():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SUM(e.Cost) as TotalRevenue
            FROM examination e
            JOIN patient_examination pe ON e.ExamID = pe.ExamID
        """)
        revenue = dict(cursor.fetchone())
        conn.close()
        return jsonify(revenue)
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route("/api/kpi/cost", methods=["GET"])
def get_cost():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SUM(e.Cost) as TotalRevenue
            FROM examination e
            JOIN patient_examination pe ON e.ExamID = pe.ExamID
        """)
        conn.close()
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route("/api/kpi/cost_per_minute", methods=["GET"])
def get_cost_per_minute():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SUM(e.Cost) / SUM(e.Duration) as CostPerMinute
            FROM examination e
            JOIN patient_examination pe ON e.ExamID = pe.ExamID
        """)
        cost_per_minute = dict(cursor.fetchone())
        conn.close()
        return jsonify(cost_per_minute)
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route("/api/kpi/examinations", methods=["GET"])
def get_examinations():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Get current month and previous month in YYYY-MM format
        cursor.execute("""
            SELECT
                strftime('%Y-%m', 'now') as current_month,
                strftime('%Y-%m', 'now', '-1 month') as previous_month
        """)
        months = cursor.fetchone()
        current_month = months["current_month"]
        previous_month = months["previous_month"]

        # Count exams for current month
        cursor.execute("""
            SELECT COUNT(*) as current
            FROM patient_examination
            WHERE strftime('%Y-%m', ExamDate) = ?
        """, (current_month,))
        current = cursor.fetchone()["current"]

        # Count exams for previous month
        cursor.execute("""
            SELECT COUNT(*) as previous
            FROM patient_examination
            WHERE strftime('%Y-%m', ExamDate) = ?
        """, (previous_month,))
        previous = cursor.fetchone()["previous"]

        conn.close()
        return jsonify({"current": current, "previous": previous})
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
