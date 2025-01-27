from fastapi import UploadFile
from api.models.patient_model import Patient
from sqlalchemy.exc import IntegrityError
from api.exceptions.invalid_input_exception import InvalidInputException
from api.helpers.image_uploader import upload_image

def create_patient(name: str, email_address: str, phone_number: str, image: UploadFile, db):
    image_path = upload_image(image)
    patient = Patient(name=name, email_address=email_address, phone_number=phone_number, image_path=image_path)
    try:
        db.add(patient)
        db.commit()
        db.refresh(patient)
    except IntegrityError:
        db.rollback()
        raise InvalidInputException("Email address already exists.")
    return patient