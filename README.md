# Secure Database-as-a-Service (DBaaS) Project

📋 Project Overview

This project implements a Secure Database-as-a-Service system designed for a "semi-trusted" cloud environment. In this model, the cloud provider (database) is assumed to be honest-but-curious: it follows protocols but attempts to learn information from stored data.

To mitigate this, the system employs a Client-Side Encryption Middleware architecture. All data encryption, decryption, and integrity hashing occur locally on the client application before data is sent to the cloud.

🛡️ Key Security Features

    User Authentication: Passwords are salted and hashed using bcrypt before storage. Plain-text passwords never touch the database .

Role-Based Access Control (RBAC):

    Group H (Health Professionals): Full access to patient data.

    Group R (Researchers): Access to statistical data only; PII (First/Last Names) is redacted .

Data Confidentiality: Sensitive attributes (Gender, Age) are encrypted using AES-128 (Fernet) with probabilistic encryption (unique IVs per row) to prevent statistical leakage .

Data Integrity: Each row includes an HMAC (Hash-Based Message Authentication Code). If the cloud provider or an attacker tampers with the data, the client detects the signature mismatch upon retrieval .

Architecture

Shutterstock

Explore

The system consists of two main components:

    Client App (Python): Handles login, encryption/decryption logic, and access control enforcement.

    Cloud Database (AWS RDS / MySQL): Stores encrypted blobs (gender_enc, age_enc) and integrity signatures.

Prerequisites

    Python 3.8+

    MySQL Server (Localhost or AWS RDS instance)

Installation & Setup

1. Clone the Repository

git clone [<repository-url>](https://github.com/ajoseph723/DSP-Project.git)
cd <repository-folder>

2.Install Dependencies

It is recommended to run this in a virtual environment.
Bash

pip install -r requirements.txt

3.Database Configuration

Open main.py and db_setup.py. Update the DB_CONFIG dictionary with your database credentials:
Python

DB_CONFIG = {
    'host': "your-database-endpoint.amazonaws.com", # or localhost
    'user': "your-username",
    'password': "your-password",
    'database': "DSP_Database"
}

4.Initialize the Database

Run the setup script to create the necessary tables (Users and Patients) and seed the initial users.
Bash

python db_setup.py

5.Generate Dummy Data

To populate the database with 100+ encrypted dummy records (using the Faker library):
Bash

python populate_db.py

🖥️ Usage

Run the main application interface:
Bash

python main.py

default Login Credentials

The system comes seeded with two default users for testing Access Control:
Role Username Password Permissions
Doctor (Group H) doctor_bob securepass123 Can View (Decrypted) & Add Patients
Researcher (Group R) researcher_alice researchpass123 Can View (Redacted Names)

Testing

Run Unit Tests

To verify cryptographic logic (hashing/encryption) and database integration:
Bash

## Test security logic (Hashing, AES, HMAC)

python test_security_logic.py

## Test database read/write operations

python test_db_integration.py

Project Structure

    main.py: The primary CLI application loop.

    security_utils.py: Core cryptographic module (AES, HMAC, Bcrypt).

    db_setup.py: Schema initialization and user seeding.

    populate_db.py: Generates encrypted dummy data for stress testing.

    secret.key: (Auto-generated) Contains the symmetric encryption key. Do not upload this to public GitHub.

Limitations

    Key Management: The symmetric key (secret.key) is currently stored locally. In a production environment, this should be managed by a Hardware Security Module (HSM) or a Key Management Service (KMS).

    Searchability: Because probabilistic encryption is used (randomized ciphertexts), the encrypted columns (Gender, Age) cannot be queried directly using SQL WHERE clauses (e.g., WHERE gender='Male' is impossible).

    Concurrency: The current integrity check is per-row. It does not strictly prevent "Rollback Attacks" (cloud restoring an old version of the whole table).
