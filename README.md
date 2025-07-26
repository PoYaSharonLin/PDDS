# 2025 Programming for Data-Driven System 

## TA Materials
PDDS TA Course Materials: https://hackmd.io/@PoYa-Sharon-Lin/ryJmKZOBxe 

## Branch Description 
This branch contains the backend, frontend, and the database for the PDDS course project.


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

### 5. Run Dash (frontend)
```bash
python app.py
```

## Additional Installation 

- SQLite Browser: for viewing the SQLite database
- Postman: for debugging the API endpoint

