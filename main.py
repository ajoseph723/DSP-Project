# !/usr/bin/env python3
#
# main.py
#
# Description: Implements secure login, data retrieval with integrity checks,
# and data addition with encryption and integrity signatures.
#
# 11/24/2025
#

import mysql.connector
from security_utils import SecurityManager
import sys

# Database Configuration
DB_CONFIG = {
    "host": "dsp-mysqldatabase.chogg206kt6s.us-east-2.rds.amazonaws.com",
    "user": "admin",
    "password": "Kent2025",
    "database": "DSP_Database",
}


def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"Error connecting to DB: {err}")
        sys.exit(1)


def login(cursor, sec_manager):
    """
    Handles User Authentication.
    Verifies hash against the database.
    """
    print("\n--- SECURE LOGIN ---")
    username = input("Username: ")
    password = input("Password: ")

    # Fetch the user's stored hash and role
    query = "SELECT password_hash, role FROM Users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result:
        stored_hash = result[0]
        role = result[1]

        # Verify password using bcrypt
        if sec_manager.verify_password(password, stored_hash):
            print(f"Login Successful! Role: {role}")
            return username, role

    print("Invalid credentials.")
    return None, None


def view_patients(cursor, sec_manager, user_role):
    """
    Handles Data Retrieval, Integrity Checking, and Access Control.
    
    """
    print(f"\n--- PATIENT RECORDS (Role: {user_role}) ---")

    # Fetch data from DB
    query = """SELECT id, first_name, last_name, gender_enc, age_enc, 
               weight, height, history, row_signature FROM Patients"""
    cursor.execute(query)
    rows = cursor.fetchall()

    if not rows:
        print("No records found.")
        return

    print(
        f"{'ID':<4} {'Name':<20} {'Gender':<10} {'Age':<5} {'Weight':<8} {'History':<20} {'Integrity':<10}"
    )
    print("-" * 90)

    for row in rows:
        r_id, fname, lname, gender_enc, age_enc, weight, height, history, stored_sig = (
            row
        )

        # Integrity Check
        # Reconstruct the string used for hashing
        # We ensure all fields are strings to match the signature generation

        raw_data_string = (
            f"{fname}{lname}{gender_enc}{age_enc}{weight}{height}{history}"
        )

        calculated_sig = sec_manager.generate_integrity_signature(raw_data_string)

        integrity_status = "OK"
        if stored_sig != calculated_sig:
            integrity_status = "FAIL (TAMPERED)"

        # Decryption
        # Decrypt Gender and Age locally
        try:
            gender_plain = sec_manager.decrypt_data(gender_enc)
            age_plain = sec_manager.decrypt_data(age_enc)
        except:
            gender_plain = "ERR"
            age_plain = "ERR"

        # Access Control
        # If user is a Researcher then hide names
        display_name = f"{fname} {lname}"
        if user_role == "R":
            display_name = "REDACTED"

        # Display the row
        print(
            f"{r_id:<4} {display_name:<20} {gender_plain:<10} {age_plain:<5} {weight:<8} {history:<20} {integrity_status:<10}"
        )


def add_patient(cursor, db, sec_manager):
    """
    Allows Group H to add new encrypted records.

    """
    print("\n--- ADD NEW PATIENT ---")
    fname = input("First Name: ")
    lname = input("Last Name: ")
    gender = input("Gender: ")
    age = input("Age: ")
    weight = float(input("Weight: "))
    height = float(input("Height: "))
    history = input("History: ")

    # Encryption
    # Encrypt sensitive fields before they leave the client
    gender_enc = sec_manager.encrypt_data(gender).decode("utf-8")
    age_enc = sec_manager.encrypt_data(age).decode("utf-8")

    # Integrity check
    # Create HMAC of the row data
    raw_data_string = f"{fname}{lname}{gender_enc}{age_enc}{weight}{height}{history}"
    row_sig = sec_manager.generate_integrity_signature(raw_data_string)

    # Upload to DB
    query = """INSERT INTO Patients 
               (first_name, last_name, gender_enc, age_enc, weight, height, history, row_signature)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    values = (fname, lname, gender_enc, age_enc, weight, height, history, row_sig)

    try:
        cursor.execute(query, values)
        db.commit()
        print("Patient added successfully.")
    except mysql.connector.Error as err:
        print(f"Error adding patient: {err}")


def main():
    sec_manager = SecurityManager("secret.key")
    db = get_db_connection()
    cursor = db.cursor()

    # Login
    current_user, current_role = login(cursor, sec_manager)

    if not current_user:
        return  # Exit if login fails

    # Main menu loop
    while True:
        print(f"\nLogged in as: {current_user} (Group {current_role})")
        print("1. View Patients")
        if current_role == "H":
            print("2. Add Patient")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            view_patients(cursor, sec_manager, current_role)

        elif choice == "2":
            if current_role == "H":
                add_patient(cursor, db, sec_manager)
            else:
                print("Access Denied: Only Group H can add patients.")

        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid option.")

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
