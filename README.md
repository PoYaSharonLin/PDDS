# 2025 Programming for Data-Driven System 

## TA Materials
PDDS TA Course Materials: https://hackmd.io/@PoYa-Sharon-Lin/ryJmKZOBxe 

## Branch Description 
This repo provides the material for the TA Course regarding Database Demo: https://hackmd.io/@PoYa-Sharon-Lin/Hy4d0VwLll.
We start by taking a look at our raw data and then we will undergo the normalization process using python. 
After that, we would receive 6 clean csv tables, which we can import to DB Browser. 
To test whether the connection is successfully connected, we recommend using the provided sql. 

The 2 `.db` files serves as the demo of how the database would look like after preforming the queries. 
Students should create their own `.db` file while using DB browser. 

### File Structure 
```bash
Database-Demo/
├── README.md
├── hospital_database.db              # db for not using GUI (DB Browser)
├── hospital_database_dbbrowser.db    # db for using DB Browser
├── normalization.py                  # Process of normalizing the tables 
├── query.sql                         # SQL queries for testing connection & operations
└── system_data.xlsx                  # Raw data in xlsx format 
```

