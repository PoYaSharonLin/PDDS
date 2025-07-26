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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
