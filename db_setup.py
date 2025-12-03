# !/usr/bin/env python3
#
# db_setup.py
#
# Description: Initializes the MySQL database and tables for the DSP project.
# Creates Users and Patients tables with appropriate fields.
# Seeds initial dummy data for testing.
#
# 11/24/2025
#

import mysql.connector
from security_utils import SecurityManager


def init_db():
    # Connect to MySQL server
    db = mysql.connector.connect(
        host="dsp-mysqldatabase.chogg206kt6s.us-east-2.rds.amazonaws.com",
        user="admin",
        password="Kent2025",
        database="DSP_Database",
        port=3306,
    )
    cursor = db.cursor()

    # Create Database
    cursor.execute("CREATE DATABASE IF NOT EXISTS DSP_Database")
    cursor.execute("USE DSP_Database")

    # Create Users Table
    # Stores username, hashed password, and Role (H or R)
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE,
        password_hash VARCHAR(255),
        role CHAR(1)
    )
    """
    )

    # Create Patients Table
    # Gender and Age are encrypted (stored as TEXT/BLOB)
    # Row_Signature is for integrity checking
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Patients (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        gender_enc TEXT,     
        age_enc TEXT,        
        weight FLOAT,
        height FLOAT,
        history TEXT,
        row_signature VARCHAR(64)
    )
    """
    )

    print("Database and Tables Initialized Successfully.")

    # --- SEED DUMMY DATA ---
    # We must seed at least 100 items
    # We need to register at least one Group H and one Group R user
    sec = SecurityManager()

    # Check if admin exists, if not, create
    cursor.execute("SELECT * FROM Users WHERE username = 'doctor_bob'")
    if not cursor.fetchone():
        pw_hash = sec.hash_password("securepass123")
        cursor.execute(
            "INSERT INTO Users (username, password_hash, role) VALUES (%s, %s, %s)",
            ("doctor_bob", pw_hash, "H"),
        )

    cursor.execute("SELECT * FROM Users WHERE username = 'researcher_alice'")
    if not cursor.fetchone():
        pw_hash = sec.hash_password("researchpass123")
        cursor.execute(
            "INSERT INTO Users (username, password_hash, role) VALUES (%s, %s, %s)",
            ("researcher_alice", pw_hash, "R"),
        )

    db.commit()
    print("Users seeded.")

if __name__ == "__main__":
    init_db()
