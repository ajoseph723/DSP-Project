import bcrypt
from cryptography.fernet import Fernet
import hmac
import hashlib
import json


class SecurityManager:
    def __init__(self, key_file="secret.key"):
        # Load or generate a symmetric key for AES encryption
        # In a real app, this key stays with the Client, NEVER the Cloud.
        try:
            with open(key_file, "rb") as f:
                self.key = f.read()
        except FileNotFoundError:
            self.key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(self.key)

        self.cipher = Fernet(self.key)

    # Authentication
    def hash_password(self, plain_password):
        """Hashes password using bcrypt (includes salt)."""
        # [cite: 41, 42]
        return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())

    def verify_password(self, plain_password, hashed_password):
        """Verifies a stored hash against an input password."""
        # FIX: Convert the hash from DB (string) back to bytes
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode("utf-8")

        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)

    # Data Confidentiality
    def encrypt_data(self, data):
        """
        Encrypts data (e.g., Gender, Age).
        Fernet uses AES-128 in CBC mode with a random IV every time.
        This prevents statistical leakage (e.g., 'Male' will look different every time).

        """
        if isinstance(data, (int, float)):
            data = str(data)
        return self.cipher.encrypt(data.encode("utf-8"))

    def decrypt_data(self, encrypted_data):
        """Decrypts data back to string."""
        return self.cipher.decrypt(encrypted_data).decode("utf-8")

    # Integrity Protection
    def generate_integrity_signature(self, row_data_string):
        """
        Creates an HMAC signature for a row.
        If the cloud alters the data, this hash will no longer match.

        """
        return hmac.new(
            self.key, row_data_string.encode("utf-8"), hashlib.sha256
        ).hexdigest()
