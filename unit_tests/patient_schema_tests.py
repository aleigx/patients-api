import unittest
from pydantic import ValidationError
from api.schemas.patient_schema import PatientCreate
from api.exceptions.invalid_input_exception import InvalidInputException

class TestPatientCreate(unittest.TestCase):

    def test_valid_patient_create(self):
        patient = PatientCreate(
            name="John Doe",
            email_address="john.doe@example.com",
            phone_number="1234567890"
        )
        self.assertEqual(patient.name, "John Doe")
        self.assertEqual(patient.email_address, "john.doe@example.com")
        self.assertEqual(patient.phone_number, "1234567890")

    def test_invalid_phone_number(self):
        with self.assertRaises(InvalidInputException) as context:
            PatientCreate(
                name="John Doe",
                email_address="john.doe@example.com",
                phone_number="123-456-7890"
            )
        self.assertEqual(str(context.exception), "Phone number must be valid.")

    def test_invalid_email_address(self):
        with self.assertRaises(InvalidInputException) as context:
            PatientCreate(
                name="John Doe",
                email_address="john.doeexample.com",
                phone_number="1234567890"
            )
        self.assertEqual(str(context.exception), "Email address must be valid.")

if __name__ == '__main__':
    unittest.main()