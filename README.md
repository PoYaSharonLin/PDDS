# 2025 Programming for Data-Driven System 

## TA Materials
PDDS TA Course Materials: https://hackmd.io/@PoYa-Sharon-Lin/ryJmKZOBxe 

## Branch Description 
This branch contains the backend, frontend, and the database for the PDDS course project.
Most of the contents is the same as Database-Demo. 
However, here we organize the files into corresponding folders. 

---

## File Structure 
```bash
Dash-Demo-Dev/
├── preprocessing               # Process of normalizing the tables 
│   ├── DBconnection.py
│   └── normalization.py
├── query.sql
├── requirements.txt            # for packages needed to run this application 
├── src                         # Raw data in xlsx format & normalized tables 
│   ├── doctor.csv
│   ├── doctor_examination.csv
│   ├── examination.csv
│   ├── hospital_database.db    # database for testing connection 
│   ├── patient.csv
│   ├── patient_doctor.csv
│   ├── patient_examination.csv
│   └── system_data.xlsx
```
---

## Instructions 

### 1. Clone the Repository
clone the repo to local machine
```bash
git clone <repository-url>
```

open up a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
    pip install -r requirements.txt
```

### 3. Run tests 
activate api
```bash
python api.py
```

run tests 
```bash
pytest test/test_api.py
```


### 4. Run Preprocessing 
Run the command below to export the normalized tables to csv files and connect to SQLite database.

```bash
python3 preprocessing/normalization.py
```

Run the command below to add tables to SQLite database.
```bash
python3 preprocessing/DBconnection.py
```

Test SQLite connection
```bash
# cd src
sqlite3 hospital_database.db
```

```sql
# .tables
# SELECT * FROM patient LIMIT 5;
```
```sql
#  BEGIN;
#  INSERT INTO patient (FirstName, LastName, Year, Month, Day)
#  VALUES ('John', 'Doe', 1985, 6, 15);
#  COMMIT;
#  SELECT * FROM patient;
```

### 5. Run Dash (frontend)
```bash
python3 app.py
```

## Additional Installation 

- SQLite Browser: for viewing the SQLite database
- Postman: for debugging the API endpoint

## Deploy to Heroku 
```bash
heroku login
```
```bash
git add .
git commit -m "Heroku commit"
git push 
git push heroku main 
```
