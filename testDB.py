#pip install mysql-connector-python

import os
import mysql.connector

# Establish connection object to database
conn = mysql.connector.connect(
    host="dsp-mysqldatabase.chogg206kt6s.us-east-2.rds.amazonaws.com",
    user="admin",
    password="Kent2025",
    database="DSP_Database",
    port=3306
)
cur = conn.cursor()  # cursor is used to run queries and fetch results from DB
cur.execute("SELECT NOW();")  # returns current date and time from DB server
print(cur.fetchone())  # fetches one row from data in cursor (fetched time result is one tuple of data anyway)

# Show all data tables in db
cur.execute("SHOW TABLES;")
tables = cur.fetchall()
for t in tables:
    print(t)

# Print all data in healthcare table
cur.execute("SELECT * FROM healthcare;")
rows = cur.fetchall()
for r in rows:
    print(r)

cur.close()
conn.close()  # close DB connection
