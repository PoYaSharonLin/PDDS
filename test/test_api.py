import pytest  # type: ignore
import requests


@pytest.fixture
def base_url():
    return "http://127.0.0.1:8000"


def test_root_endpoint(base_url):
    """Test the root endpoint returns welcome message"""
    response = requests.get(f"{base_url}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Hospital API"}


def test_patients_endpoint(base_url):
    """Test the patients endpoint returns a list of patient objects"""
    response = requests.get(f"{base_url}/api/patients")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:  # Check structure only if data is not empty
        assert "PatientID" in data[0]
        assert "FirstName" in data[0]
        assert "LastName" in data[0]


def test_patients_by_doctor_endpoint(base_url):
    """Test the patients by doctor endpoint
    returns patient names or empty list"""
    response = requests.get(f"{base_url}/api/patients/doctor/D001")
    assert response.status_code in [200, 404]  # Allow 404 for no patients
    data = response.json()
    assert isinstance(data, list)
    if response.status_code == 200 and data:
        assert "FirstName" in data[0]
        assert "LastName" in data[0]


def test_patients_exam_count_endpoint(base_url):
    """Test the exam count endpoint returns patient exam counts"""
    response = requests.get(f"{base_url}/api/patients/exam-count")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "FirstName" in data[0]
        assert "LastName" in data[0]
        assert "ExamCount" in data[0]


def test_doctors_blood_test_endpoint(base_url):
    """Test the doctors blood test endpoint returns list of doctors"""
    response = requests.get(f"{base_url}/api/doctors/blood-test")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
