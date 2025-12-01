import mysql.connector
from security_utils import SecurityManager
from faker import Faker
import random

# Database Configuration
DB_CONFIG = {
    "host": "dsp-mysqldatabase.chogg206kt6s.us-east-2.rds.amazonaws.com",
    "user": "admin",
    "password": "Kent2025",
    "database": "DSP_Database",
}


def populate():
    print("--- STARTING BULK DATA GENERATION ---")

    # Setup
    fake = Faker()
    sec_manager = SecurityManager("secret.key")

    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
    except Exception as e:
        print(f"Connection Failed: {e}")
        return

    # Generate 100 records
    print("Generating and encrypting 100 records...")

    records_to_insert = []

    for _ in range(100):
        # Generate Fake Data
        fname = fake.first_name()
        lname = fake.last_name()
        gender = random.choice(["Male", "Female", "Non-binary"])
        age = str(random.randint(18, 90))
        weight = round(random.uniform(110.0, 250.0), 1)
        height = round(random.uniform(150.0, 200.0), 1)
        history = fake.sentence(nb_words=6)

        # Encryption
        # Encrypt Gender and Age using the SecurityManager
        gender_enc = sec_manager.encrypt_data(gender).decode("utf-8")
        age_enc = sec_manager.encrypt_data(age).decode("utf-8")

        # Integrity Signature
        # Generate the signature exactly how main.py expects it
        raw_data_string = (
            f"{fname}{lname}{gender_enc}{age_enc}{weight}{height}{history}"
        )
        row_sig = sec_manager.generate_integrity_signature(raw_data_string)

        records_to_insert.append(
            (fname, lname, gender_enc, age_enc, weight, height, history, row_sig)
        )

    # Bulk Insert
    query = """INSERT INTO Patients 
               (first_name, last_name, gender_enc, age_enc, weight, height, history, row_signature) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    try:
        cursor.executemany(query, records_to_insert)
        db.commit()
        print(f"Successfully inserted {cursor.rowcount} records.")
    except Exception as e:
        print(f"Insert Error: {e}")
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    populate()
