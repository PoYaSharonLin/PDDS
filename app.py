from dash import Dash, html, dcc
import plotly.graph_objects as go
import sqlite3

# --- Database Connection ---
def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect("./src/hospital_database.db")
    conn.row_factory = sqlite3.Row
    return conn

# --- Data Fetching Functions ---
def fetch_exam_counts():
    """Fetch patient examination counts directly from the database."""
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
        return counts
    except Exception as e:
        print(f"Error fetching exam counts: {e}")
        return []

def fetch_blood_test_doctors():
    """Fetch doctors performing blood tests directly from the database."""
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
        return doctors
    except Exception as e:
        print(f"Error fetching blood test doctors: {e}")
        return []

# --- Chart Creation Functions ---
def create_exam_count_bar_chart(exam_data):
    patient_names = [f"{d['FirstName']} {d['LastName']}" for d in exam_data]
    exam_counts = [d['ExamCount'] for d in exam_data]
    fig = go.Figure(data=[go.Bar(x=patient_names, y=exam_counts, text=exam_counts, textposition='auto', marker_color='rgb(55, 83, 109)')])
    fig.update_layout(title='Number of Examinations per Patient', xaxis_title='Patient Name', yaxis_title='Number of Examinations', xaxis_tickangle=-45, showlegend=False, height=500)
    return fig

def create_blood_test_doctor_pie_chart(doctor_data):
    doctor_names = [f"{d['Title']} {d['FirstName']} {d['LastName']}" for d in doctor_data]
    doctor_counts = {}
    for name in doctor_names:
        doctor_counts[name] = doctor_counts.get(name, 0) + 1
    fig = go.Figure(data=[go.Pie(labels=list(doctor_counts.keys()), values=list(doctor_counts.values()), textinfo='label+percent', insidetextorientation='radial')])
    fig.update_layout(title='Distribution of Doctors Performing Blood Tests', showlegend=True, height=500)
    return fig

# --- Main Application Setup ---
app = Dash(__name__)
server = app.server # Expose the server for Gunicorn

# --- Fetch Data and Create Figures ---
exam_data = fetch_exam_counts()
doctor_data = fetch_blood_test_doctors()

bar_fig = create_exam_count_bar_chart(exam_data) if exam_data else go.Figure()
pie_fig = create_blood_test_doctor_pie_chart(doctor_data) if doctor_data else go.Figure()

# --- Define Layout (KPI Section is now gone) ---
app.layout = html.Div([
    html.H1("Hospital Data Dashboard", style={'textAlign': 'center'}),
    html.Div([
        dcc.Graph(id='exam-bar-chart', figure=bar_fig, style={'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(id='doctor-pie-chart', figure=pie_fig, style={'width': '50%', 'display': 'inline-block'})
    ]),
])

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)