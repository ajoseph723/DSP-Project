import sys
import os

current_dir = os.path.dirname(
    os.path.abspath(__file__)
)  # Get the absolute path of the current file's directory
project_path = os.path.abspath(
    os.path.join(current_dir, "..")
)  # Set file path
os.chdir(project_path)  # Change the working directory to GammaRepo
sys.path.append(project_path)

import mysql.connector
from security_utils import SecurityManager

def test_db_cycle():
    print("--- Starting Database Integration Test ---")

    # 1. Connect
    try:
        db = mysql.connector.connect(
            host="dsp-mysqldatabase.chogg206kt6s.us-east-2.rds.amazonaws.com",
            user="admin",
            password="Kent2025",
            database="DSP_Database",
            port=3306,
        )
        cursor = db.cursor()
        print("[PASS] Database Connected.")
    except Exception as e:
        print(f"[FAIL] Could not connect to DB: {e}")
        return

    sec = SecurityManager("test_secret.key")

    # Pretend this is user input
    pt_gender = "Female"
    pt_age = "29"

    # Encrypt Data
    enc_gender = sec.encrypt_data(pt_gender)
    enc_age = sec.encrypt_data(pt_age)

    # Create Integrity Signature
    
    raw_blob = pt_gender + pt_age
    row_sig = sec.generate_integrity_signature(raw_blob)

    # Insert into DB
    try:
        sql = """INSERT INTO Patients 
                 (first_name, last_name, gender_enc, age_enc, weight, height, history, row_signature) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        val = ("Test", "User", enc_gender, enc_age, 70.5, 170.0, "No history", row_sig)

        cursor.execute(sql, val)
        db.commit()
        test_id = cursor.lastrowid
        print(f"[PASS] Inserted Test Row ID: {test_id}")
    except Exception as e:
        print(f"[FAIL] Insert Failed: {e}")
        return

    # Retrieve and Verify
    try:
        cursor.execute(
            "SELECT gender_enc, age_enc, row_signature FROM Patients WHERE id = %s",
            (test_id,),
        )
        result = cursor.fetchone()

        if not result:
            print("[FAIL] Row not found.")
            return

        db_gender_enc, db_age_enc, db_sig = result

        # Decrypt
        dec_gender = sec.decrypt_data(db_gender_enc)
        dec_age = sec.decrypt_data(db_age_enc)

        print(f"   Fetched Encrypted Gender: {db_gender_enc[:15]}...")  # Show snippet
        print(f"   Decrypted Gender: {dec_gender}")

        # Verify Integrity
        # Re-calculate hash based on what was just decrypted
        recalc_sig = sec.generate_integrity_signature(dec_gender + dec_age)

        if dec_gender == pt_gender and dec_age == pt_age:
            print("[PASS] Decryption matches original data.")
        else:
            print("[FAIL] Decryption mismatch.")

        if db_sig == recalc_sig:
            print("[PASS] Integrity Signature Valid.")
        else:
            print("[FAIL] Integrity Check Failed (Data corrupted).")

        # Delete the test row
        cursor.execute("DELETE FROM Patients WHERE id = %s", (test_id,))
        db.commit()
        print("[PASS] Cleanup complete.")

    except Exception as e:
        print(f"[FAIL] Retrieval/Verification Error: {e}")


if __name__ == "__main__":
    test_db_cycle()
