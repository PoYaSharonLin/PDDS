-- Insert Patient data
INSERT INTO patient (FirstName, LastName, Year, Month, Day)
VALUES ('John', 'Doe', 1985, 6, 15);
SELECT * FROM patient;

-- Retrieve all patients assigned to a specific doctor
SELECT p.FirstName, p.LastName
FROM patient p
JOIN patient_doctor pd ON p.PatientID = pd.PatientID
WHERE pd.DoctorID = "D001";


-- Count the number of examinations per patient
SELECT p.FirstName, p.LastName, COUNT(pe.ExamID) AS ExamCount
FROM patient p
LEFT JOIN patient_examination pe ON p.PatientID = pe.PatientID
GROUP BY p.PatientID, p.FirstName, p.LastName;

-- Find all doctors who performed 'Blood Test'
SELECT d.Title, d.FirstName, d.LastName
FROM doctor d
JOIN doctor_examination de ON d.DoctorID = de.DoctorID
JOIN examination e ON de.ExamID = e.ExamID
WHERE e.ExamType = 'Blood Test';