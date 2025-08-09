from dash import Dash, html, dcc  # type: ignore
import plotly.graph_objects as go   # type: ignore
import requests

app = Dash(__name__)

# Base URL for the API
BASE_URL = "http://localhost:8000"

class KPI:
    '''Fetch functions'''
    @staticmethod
    def fetch_revenue_data():
        '''Fetch HospitalStayDays * $1200 grouped by Month'''
        try:
            response = requests.get(f"{BASE_URL}/api/kpi/revenue")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching Hospital Stay Days: {e}")
            return []

    @staticmethod
    def fetch_cost_data():
        '''Fetch SUM(Examination Cost) / COUNT(Examination ID)'''
        try:
            response = requests.get(f"{BASE_URL}/api/kpi/cost")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching Examination cost or examination ID: {e}")
            return []

    @staticmethod
    def fetch_cost_per_minute_data():
        '''Fetch Examination Cost / Duration Minutes'''
        try:
            response = requests.get(f"{BASE_URL}/api/kpi/cost_per_minute")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching cost per minute: {e}")
            return []

    @staticmethod
    def fetch_examination_data():
        '''Fetch COUNTIF(ExamID, DateRange, "in this month")'''
        try:
            response = requests.get(f"{BASE_URL}/api/kpi/examinations")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching examination count: {e}")
            return []
            
    '''Create functions'''
    @staticmethod
    def create_revenue(revenue_data):
        '''Create an indicator for revenue data'''
        fig = go.Figure(data=[
            go.Indicator(
                mode="number+delta",
                value=revenue_data['current'],
                delta={'reference': revenue_data['previous'], 'relative': True},
                title={'text': "Revenue"},
                number={'prefix': "$"}
            )
        ])
        return fig

    @staticmethod
    def create_cost(cost_data):
        '''Create an indicator for cost data'''
        fig = go.Figure(data=[
            go.Indicator(
                mode="number+delta",
                value=cost_data['current'],
                delta={'reference': cost_data['previous'], 'relative': True},
                title={'text': "Cost"},
                number={'prefix': "$"}
            )
        ])
        return fig

    @staticmethod
    def create_cost_per_minute(cost_per_minute_data):
        '''Create an indicator for cost per minute data'''
        fig = go.Figure(data=[
            go.Indicator(
                mode="number+delta",
                value=cost_per_minute_data['current'],
                delta={'reference': cost_per_minute_data['previous'], 'relative': True},
                title={'text': "Cost per Minute"},
                number={'prefix': "$"}
            )
        ])
        return fig

    @staticmethod
    def create_examination_count(examination_data):
        '''Create an indicator for examination data'''
        fig = go.Figure(data=[
            go.Indicator(
                mode="number+delta",
                value=examination_data['current'],
                delta={'reference': examination_data['previous'], 'relative': True},
                title={'text': "Examination Count"}
            )
        ])
        return fig

class KPI:
    @staticmethod
    def fetch_revenue_data():
        '''Fetch HospitalStayDays * $1200 grouped by Month'''
        try:
            response = requests.get(f"{BASE_URL}/api/kpi/revenue")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching Hospital Stay Days: {e}")
            return []

    @staticmethod
    def fetch_cost_data():
        '''Fetch SUM(Examination Cost) / COUNT(Examination ID)'''
        try:
            response = requests.get(f"{BASE_URL}/api/kpi/cost")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching Examination cost or examination ID: {e}")
            return []

    @staticmethod
    def fetch_cost_per_minute_data():
        '''Fetch Examination Cost / Duration Minutes'''
        try:
            response = requests.get(f"{BASE_URL}/api/kpi/cost_per_minute")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching cost per minute: {e}")
            return []

    @staticmethod
    def fetch_examination_data():
        '''Fetch COUNTIF(ExamID, DateRange, "in this month")'''
        try:
            response = requests.get(f"{BASE_URL}/api/kpi/examinations")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching examination count: {e}")
            return []

    @staticmethod
    def create_revenue(revenue_data):
        '''Create an indicator for revenue data'''
        fig = go.Figure(data=[
            go.Indicator(
                mode="number+delta",
                value=revenue_data['current'],
                delta={'reference': revenue_data['previous'], 'relative': True},
                title={'text': "Revenue"},
                number={'prefix': "$"}
            )
        ])
        return fig

    @staticmethod
    def create_cost(cost_data):
        '''Create an indicator for cost data'''
        fig = go.Figure(data=[
            go.Indicator(
                mode="number+delta",
                value=cost_data['current'],
                delta={'reference': cost_data['previous'], 'relative': True},
                title={'text': "Cost"},
                number={'prefix': "$"}
            )
        ])
        return fig

    @staticmethod
    def create_cost_per_minute(cost_per_minute_data):
        '''Create an indicator for cost per minute data'''
        fig = go.Figure(data=[
            go.Indicator(
                mode="number+delta",
                value=cost_per_minute_data['current'],
                delta={'reference': cost_per_minute_data['previous'], 'relative': True},
                title={'text': "Cost per Minute"},
                number={'prefix': "$"}
            )
        ])
        return fig

    @staticmethod
    def create_examination_count(examination_data):
        '''Create an indicator for examination data'''
        fig = go.Figure(data=[
            go.Indicator(
                mode="number+delta",
                value=examination_data['current'],
                delta={'reference': examination_data['previous'], 'relative': True},
                title={'text': "Examination Count"}
            )
        ])
        return fig


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
<<<<<<< HEAD
revenue_data = fetch_revenue_data()
cost_data = fetch_cost_data()
cost_per_minute_data = fetch_cost_per_minute_data()
examination_data = fetch_examination_data()
=======
kpi = KPI()
revenue_data = kpi.fetch_revenue_data()
cost_data = kpi.fetch_cost_data()
cost_per_minute_data = kpi.fetch_cost_per_minute_data()
examination_data = kpi.fetch_examination_data()
>>>>>>> 47cdc03 (add: add KPI functions for fetching data and creating fig)

# Create figures
bar_fig = create_exam_count_bar_chart(exam_data) if exam_data else go.Figure()
pie_fig = (
    create_blood_test_doctor_pie_chart(doctor_data)
    if doctor_data else go.Figure()
)
<<<<<<< HEAD
revenue_fig = KPI.create_revenue(revenue_data)
average_cost_fig = KPI.create_cost(cost_data)
cost_per_minutes_fig = KPI.create_cost_per_minute(cost_per_minute_data)
examination_count_fig = KPI.create_examination_count(examination_data)

=======
revenue_fig = kpi.create_revenue(revenue_data)
average_cost_fig = kpi.create_cost(cost_data)
cost_per_minutes_fig = kpi.create_cost_per_minute(cost_per_minute_data)
examination_count_fig = kpi.create_examination_count(examination_data)
>>>>>>> 47cdc03 (add: add KPI functions for fetching data and creating fig)

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
    ]),
<<<<<<< HEAD
    html.H2("KPIs Overview", style={'textAlign':'center'}),
    html.Div([
        dcc.Graph(
            id='hospital-revenue-indicator',
            figure=revenue_fig, 
=======
    html.H2("KPIs Overview", style={'textAlign': 'center'}),
    html.Div([
        dcc.Graph(
            id='hospital-revenue-indicator',
            figure=revenue_fig,
>>>>>>> 47cdc03 (add: add KPI functions for fetching data and creating fig)
            style={
                'width': '30%',
                'display': 'inline-block'
            }
<<<<<<< HEAD
        ), 
        dcc.Graph(
            id='average-cost-indicator', 
            figure=average_cost_fig, 
            style={
                'width': '15%', 
                'display': 'inline-block'
            }
        ),
        
=======
        ),
        dcc.Graph(
            id='average-cost-indicator',
            figure=average_cost_fig,
            style={
                'width': '15%',
                'display': 'inline-block'
            }
        ),
>>>>>>> 47cdc03 (add: add KPI functions for fetching data and creating fig)
        dcc.Graph(
            id='cost-per-minute-indicator',
            figure=cost_per_minutes_fig,
            style={
<<<<<<< HEAD
                'width': '15%'
                'display': 'inline-block'
            }
        ), 
        
=======
                'width': '15%',
                'display': 'inline-block'
            }
        ),
>>>>>>> 47cdc03 (add: add KPI functions for fetching data and creating fig)
        dcc.Graph(
            id='examination-count-indicator',
            figure=examination_count_fig,
            style={
<<<<<<< HEAD
                'width': '10%', 
                'display': 'inline-block'
            }
        )
    ])
=======
                'width': '10%',
                'display': 'inline-block'
            }
        ),
    ]),
>>>>>>> 47cdc03 (add: add KPI functions for fetching data and creating fig)
])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
