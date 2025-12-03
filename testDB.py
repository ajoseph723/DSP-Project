# !/usr/bin/env python3
#
# testDB.py
# pip install mysql-connector-python
#
# Description: Simple test script to connect to the DSP_Database
# and fetch the current date and time from the MySQL server.
# 11/24/2025
#

import os
import mysql.connector

# Establishes connection object to database
conn = mysql.connector.connect(
    host="dsp-mysqldatabase.chogg206kt6s.us-east-2.rds.amazonaws.com",
    user="admin",
    password="Kent2025",
    database="DSP_Database",
    port=3306
)
cur = conn.cursor() # cursor is used to run queries and fetch results from DB
cur.execute("SELECT NOW();") # returns current date and time from DB server
print(cur.fetchone()) #fetches one row from data in cursor (fetched time result is one tuple of data anyway)
cur.close()
conn.close() # close DB connection
