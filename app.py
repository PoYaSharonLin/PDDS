from dash import Dash, html, dcc  # type: ignore
import plotly.graph_objects as go   # type: ignore
import requests

app = Dash(__name__)

# Base URL for the API
BASE_URL = "http://localhost:8000"


def fetch_exam_counts():
    """Fetch patient examination counts from the API"""
    try:
        response = requests.get(f"{BASE_URL}/api/patients/exam-count")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching exam counts: {e}")
        return []


def fetch_blood_test_doctors():
    """Fetch doctors performing blood tests from the API"""
    try:
        response = requests.get(f"{BASE_URL}/api/doctors/blood-test")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching blood test doctors: {e}")
        return []


def create_exam_count_bar_chart(exam_data):
    """Create a bar chart for patient examination counts"""
    patient_names = [f"{d['FirstName']} {d['LastName']}" for d in exam_data]
    exam_counts = [d['ExamCount'] for d in exam_data]
    fig = go.Figure(data=[
        go.Bar(
            x=patient_names,
            y=exam_counts,
            text=exam_counts,
            textposition='auto',
            marker_color='rgb(55, 83, 109)'
        )
    ])
    fig.update_layout(
        title='Number of Examinations per Patient',
        xaxis_title='Patient Name',
        yaxis_title='Number of Examinations',
        xaxis_tickangle=-45,
        showlegend=False,
        height=500
    )
    return fig


def create_blood_test_doctor_pie_chart(doctor_data):
    """Create a pie chart for doctors performing blood tests"""
    doctor_names = [
        f"{d['Title']} {d['FirstName']} {d['LastName']}"
        for d in doctor_data
    ]
    doctor_counts = {}
    for name in doctor_names:
        doctor_counts[name] = doctor_counts.get(name, 0) + 1
    fig = go.Figure(data=[
        go.Pie(
            labels=list(doctor_counts.keys()),
            values=list(doctor_counts.values()),
            textinfo='label+percent',
            insidetextorientation='radial'
        )
    ])
    fig.update_layout(
        title='Distribution of Doctors Performing Blood Tests',
        showlegend=True,
        height=500
    )
    return fig


# Fetch data
exam_data = fetch_exam_counts()
doctor_data = fetch_blood_test_doctors()

# Create figures
bar_fig = create_exam_count_bar_chart(exam_data) if exam_data else go.Figure()
pie_fig = (
    create_blood_test_doctor_pie_chart(doctor_data)
    if doctor_data else go.Figure()
)

# Define layout
app.layout = html.Div([
    html.H1("Hospital Data Dashboard", style={'textAlign': 'center'}),
    html.Div([
        dcc.Graph(
            id='exam-bar-chart',
            figure=bar_fig,
            style={
                'width': '50%',
                'display': 'inline-block'
            }
        ),
        dcc.Graph(
            id='doctor-pie-chart',
            figure=pie_fig,
            style={
                'width': '50%',
                'display': 'inline-block'
            }
        )
    ])
])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
