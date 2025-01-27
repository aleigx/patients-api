import requests
import unittest
import os
import uuid

BASE_URL = "http://localhost:8000/api/patients"

class TestAddPatient(unittest.TestCase):

    def setUp(self):
        with open("test.jpg", "wb") as f:
            f.write(b"fake_image_data")

    def test_add_patient_success(self):
        guid = str(uuid.uuid4())
        payload = {
            "name": "John Doe",
            "email_address": f"{guid}@test.com",
            "phone_number": "1234567890",
        }
        response = requests.post(BASE_URL, data=payload, files={"image": ("test.jpg", open("test.jpg", "rb"), "image/jpeg")})
        print(response.json())
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def test_add_patient_invalid_email(self):
        payload = {
            "name": "John Doe",
            "email_address": "testtest.com",
            "phone_number": "1234567890",
        }
        response = requests.post(BASE_URL, data=payload, files={"image": ("test.jpg", open("test.jpg", "rb"), "image/jpeg")})
        self.assertEqual(response.status_code, 400)

    def test_add_patient_invalid_phone(self):
        payload = {
            "name": "John Doe",
            "email_address": "test@test.com",
            "phone_number": "123-456-7890",
        }
        response = requests.post(BASE_URL, data=payload, files={"image": ("test.jpg", open("test.jpg", "rb"), "image/jpeg")})
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        os.remove("test.jpg")

        

if __name__ == "__main__":
    unittest.main()