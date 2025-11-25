import mysql.connector


def view_data():
    try:
        db = mysql.connector.connect(
            host="dsp-mysqldatabase.chogg206kt6s.us-east-2.rds.amazonaws.com",
            user="admin",
            password="Kent2025",
            database="DSP_Database",
            port=3306,
        )
        cursor = db.cursor()

        # Check Users
        print("--- USERS ---")
        cursor.execute("SELECT username, role, password_hash FROM Users")
        for row in cursor.fetchall():
            print(f"User: {row[0]} | Role: {row[1]} | Hash: {row[2][:10]}...")

        print("\n--- PATIENTS (First 5) ---")
        # Check Patients
        cursor.execute("SELECT first_name, gender_enc, age_enc FROM Patients LIMIT 5")
        for row in cursor.fetchall():
            print(
                f"Name: {row[0]} | Gender (Enc): {str(row[1])[:15]}... | Age (Enc): {str(row[2])[:15]}..."
            )

    except mysql.connector.Error as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    view_data()
