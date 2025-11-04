import pandas as pd

# 01 Read excel file
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Auto-adjust width to fit content

# Option 1: load individual sheet
source = './src/system_data.xlsx'
# patient_df = pd.read_excel(source, sheet_name='patient')
# doctor_df = pd.read_excel(source, sheet_name='doctor')
# exam_df = pd.read_excel(source, sheet_name='examination')
# print(repr(patient_df))

# Option 2: load sheets in a dictionary # Load all sheets into a dictionary
sheets = pd.read_excel(source, sheet_name=None)
# key: sheet name, value: df
# for sheet_name, df in sheets.items():
#     print(f"\nDataFrame from sheet: {sheet_name}")
#     print(repr(df))
# ----------------------------------------------------------------------------

# 02 Many-to-many relationship
# 1. patient_doctor
patient = sheets["patient"].drop(columns=['AssignedDoctors']).copy()
# print(patient)

patient_doctor = sheets["patient"][["PatientID", "AssignedDoctors"]].copy()
patient_doctor["AssignedDoctors"] = patient_doctor["AssignedDoctors"].str.split(",").apply(lambda id_list: [id.strip() for id in id_list])  # noqa: E501
patient_doctor = patient_doctor.explode("AssignedDoctors")
patient_doctor = patient_doctor.reset_index(drop=True)
# print(patient_doctor)

doctor = sheets["doctor"].drop(columns=['AssignedPatients']).copy()
# print(doctor)

# 2. patient_examination
examination = sheets["examination"].drop(columns=["PatientIDs", "PatientNames", "ResultStatus"]).copy()  # noqa: E501
# print(examination)

patient_examination = sheets["examination"][["ExamID", "PatientIDs", "ResultStatus"]].copy()  # noqa: E501
patient_examination["PatientIDs"] = patient_examination["PatientIDs"].str.split(",").apply(lambda id_list: [id.strip() for id in id_list])  # noqa: E501
patient_examination["ResultStatus"] = patient_examination["ResultStatus"].str.split(",").apply(lambda id_list: [id.strip() for id in id_list])  # noqa: E501
patient_examination = patient_examination.explode("PatientIDs")
patient_examination = patient_examination.explode("ResultStatus")
patient_examination = patient_examination.drop_duplicates()
patient_examination = patient_examination.reset_index(drop=True)
# print(patient_examination)

# 3. doctor_examication
examination = examination.drop(columns=["DoctorID", "DoctorName"])
# print(examination)

doctor_examination = sheets["examination"][["ExamID", "DoctorID"]].copy()
# print(doctor_examination)
# ----------------------------------------------------------------------------

# 03 Atomic values
# 1. patient
patient[['FirstName', 'LastName']] = patient['PatientName'].str.split(' ', expand=True)  # noqa: E501
patient['LastVisitDate'] = pd.to_datetime(patient['LastVisitDate'])
patient['Year'] = patient['LastVisitDate'].dt.year
patient['Month'] = patient['LastVisitDate'].dt.month
patient['Day'] = patient['LastVisitDate'].dt.day
patient = patient.drop(['PatientName', 'LastVisitDate'], axis=1)
# print(patient)

# 2. doctor
doctor[['Title', 'FirstName', 'LastName']] = doctor['DoctorName'].str.split(' ', expand=True)  # noqa: E501
doctor['FirstName'] = doctor['FirstName'].str.strip('.')
doctor = doctor.drop('DoctorName', axis=1)
# print(doctor)

# 3. examination
examination['ExamDate'] = pd.to_datetime(examination['ExamDate'])
examination['Year'] = examination['ExamDate'].dt.year
examination['Month'] = examination['ExamDate'].dt.month
examination['Day'] = examination['ExamDate'].dt.day
examination = examination.drop('ExamDate', axis=1)
# print(examination)
# ----------------------------------------------------------------------------

# 04 Export csv
patient.to_csv('./src/patient.csv', index=False)
doctor.to_csv('./src/doctor.csv', index=False)
examination.to_csv('./src/examination.csv', index=False)
patient_doctor.to_csv('./src/patient_doctor.csv', index=False)
patient_examination.to_csv('./src/patient_examination.csv', index=False)
doctor_examination.to_csv('./src/doctor_examination.csv', index=False)
