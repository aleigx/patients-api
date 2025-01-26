from fastapi import APIRouter, Form, UploadFile, File, Depends
from api.schemas.patient_schema import PatientCreate, parse_form_data
from api.services.patients_service import create_patient
from pydantic import EmailStr
from api.db.database import get_db

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/patients")
async def post_patient(data: dict = Depends(parse_form_data), db=Depends(get_db)):
    patient = PatientCreate(**data)
    image = data["image"]
    return create_patient(patient.name, patient.email_address, patient.phone_number, image, db)