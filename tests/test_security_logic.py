# !/usr/bin/env python3
#
# test_security_logic.py
#
# run: python3 tests/test_security_logic.py
#
# Description: Unit tests for security logic (hashing, encryption, integrity)
#
# 11/25/2025
#

import sys
import os

current_dir = os.path.dirname(
    os.path.abspath(__file__)
)  # Get the absolute path of the current file's directory
project_path = os.path.abspath(os.path.join(current_dir, ".."))  # Set file path
os.chdir(project_path)  # Change the working directory to the project root
sys.path.append(project_path)

import unittest
from security_utils import SecurityManager


class TestSecurityManager(unittest.TestCase):
    def setUp(self):
        self.sec = SecurityManager("test_secret.key")

    def test_password_hashing(self):
        """Test that passwords are hashed and salted correctly."""
        password = "my_secure_password"
        hashed = self.sec.hash_password(password)

        # Ensure hash is NOT the plain password
        self.assertNotEqual(password, hashed)

        # Ensure verification works
        self.assertTrue(self.sec.verify_password(password, hashed))

        # Ensure wrong password fails
        self.assertFalse(self.sec.verify_password("wrong_password", hashed))

    def test_probabilistic_encryption(self):
        """Test that encrypting the same data twice results in DIFFERENT ciphertexts."""
        sensitive_data = "Male"

        enc1 = self.sec.encrypt_data(sensitive_data)
        enc2 = self.sec.encrypt_data(sensitive_data)

        # Ciphertexts must look different, requirement to hide statistical info
        self.assertNotEqual(enc1, enc2)

        # Both must decrypt to the same original value
        self.assertEqual(self.sec.decrypt_data(enc1), sensitive_data)
        self.assertEqual(self.sec.decrypt_data(enc2), sensitive_data)

    def test_integrity_hmac(self):
        """Test that modifying data changes the signature."""
        data = "JohnDoeData"
        sig1 = self.sec.generate_integrity_signature(data)

        # Same data equals to same signature
        sig2 = self.sec.generate_integrity_signature(data)
        self.assertEqual(sig1, sig2)

        # Modified data should have a different signature
        sig3 = self.sec.generate_integrity_signature("JohnDoeData_Hack")
        self.assertNotEqual(sig1, sig3)


if __name__ == "__main__":
    print("Running Security Logic Tests...")
    unittest.main()
