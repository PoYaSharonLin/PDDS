import pandas as pd
import sqlite3

# Read csv file
patient = pd.read_csv('./src/patient.csv')
doctor = pd.read_csv('./src/doctor.csv')
examination = pd.read_csv('./src/examination.csv')
patient_doctor = pd.read_csv('./src/patient_doctor.csv')
patient_examination = pd.read_csv('./src/patient_examination.csv')
doctor_examination = pd.read_csv('./src/doctor_examination.csv')

# Connect to SQLite database (creates a new file if it doesn't exist)
conn = sqlite3.connect('./src/hospital_database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS patient (
    PatientID INTEGER PRIMARY KEY,
    FirstName TEXT,
    LastName TEXT,
    Year INTEGER,
    Month INTEGER,
    Day INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS doctor (
    DoctorID INTEGER PRIMARY KEY,
    Title TEXT,
    FirstName TEXT,
    LastName TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS examination (
    ExamID INTEGER PRIMARY KEY,
    ExamType TEXT,
    Year INTEGER,
    Month INTEGER,
    Day INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS patient_doctor (
    PatientID INTEGER,
    DoctorID INTEGER,
    PRIMARY KEY (PatientID, DoctorID),
    FOREIGN KEY (PatientID) REFERENCES patient(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES doctor(DoctorID)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS patient_examination (
    ExamID INTEGER,
    PatientID INTEGER,
    ResultStatus TEXT,
    PRIMARY KEY (ExamID, PatientID),
    FOREIGN KEY (ExamID) REFERENCES examination(ExamID),
    FOREIGN KEY (PatientID) REFERENCES patient(PatientID)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS doctor_examination (
    ExamID INTEGER,
    DoctorID INTEGER,
    PRIMARY KEY (ExamID, DoctorID),
    FOREIGN KEY (ExamID) REFERENCES examination(ExamID),
    FOREIGN KEY (DoctorID) REFERENCES doctor(DoctorID)
)
''')

# Export DataFrames to SQLite
patient.to_sql('patient', conn, if_exists='replace', index=False)
doctor.to_sql('doctor', conn, if_exists='replace', index=False)
examination.to_sql('examination', conn, if_exists='replace', index=False)
patient_doctor.rename(columns={'AssignedDoctors': 'DoctorID'}).to_sql('patient_doctor', conn, if_exists='replace', index=False)  # noqa: E501
patient_examination.rename(columns={'PatientIDs': 'PatientID'}).to_sql('patient_examination', conn, if_exists='replace', index=False)  # noqa: E501
doctor_examination.to_sql('doctor_examination', conn, if_exists='replace', index=False)  # noqa: E501

# Commit changes and close connection
conn.commit()
conn.close()
