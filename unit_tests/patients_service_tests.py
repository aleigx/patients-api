import unittest
from unittest.mock import MagicMock, patch
from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError
import os
with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///./test.db"}):
    from api.models.patient_model import Patient
from api.services.patients_service import create_patient
from api.exceptions.invalid_input_exception import InvalidInputException

class TestCreatePatient(unittest.TestCase):

    def setUp(self):
        self.mock_db = MagicMock()
        self.mock_upload_file = MagicMock(spec=UploadFile)
        self.mock_upload_file.filename = "test_image.jpg"
        self.mock_upload_file.file = MagicMock()
        self.mock_upload_file.file.read.return_value = b"fake_image_data"

    @patch('api.services.patients_service.upload_image', return_value="images/test_image.jpg")
    def test_create_patient_success(self, mock_upload_image):
        self.mock_db.add.return_value = None
        self.mock_db.commit.return_value = None
        self.mock_db.refresh.return_value = None

        patient = create_patient("John Doe", "john.doe@example.com", "1234567890", self.mock_upload_file, self.mock_db)

        self.assertEqual(patient.name, "John Doe")
        self.assertEqual(patient.email_address, "john.doe@example.com")
        self.assertEqual(patient.phone_number, "1234567890")
        self.assertEqual(patient.image_path, "images/test_image.jpg")
        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()

    @patch('api.services.patients_service.upload_image', return_value="images/test_image.jpg")
    def test_create_patient_integrity_error(self, mock_upload_image):
        self.mock_db.add.side_effect = IntegrityError(statement=None, params=None, orig=None)

        with self.assertRaises(InvalidInputException) as context:
            create_patient("John Doe", "john.doe@example.com", "1234567890", self.mock_upload_file, self.mock_db)

        self.assertEqual(str(context.exception), "Email address already exists.")
        self.mock_db.rollback.assert_called_once()

if __name__ == '__main__':
    unittest.main()