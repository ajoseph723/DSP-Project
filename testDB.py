#pip install mysql-connector-python

import os
import mysql.connector

# establishes connection object to database
conn = mysql.connector.connect(
    host="dsp-mysqldatabase.chogg206kt6s.us-east-2.rds.amazonaws.com",
    user="admin",
    password="Kent2025",
    database="DSP_Database",
    port=3306
)
cur = conn.cursor() #cursor is used to run queries and fetch results from DB
cur.execute("SELECT NOW();") #returns current date and time from DB server
print(cur.fetchone()) #fetches one row from data in cursor (fetched time result is one tuple of data anyway)
cur.close()
conn.close() #close DB connection
