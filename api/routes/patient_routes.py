from fastapi import APIRouter, Depends, BackgroundTasks
from api.schemas.patient_schema import PatientCreate, parse_form_data
from api.services.patients_service import create_patient
from pydantic import EmailStr
from api.db.database import get_db
from api.notification_senders.notifications_handler import handle_notifications

router = APIRouter(prefix="/api/patients", tags=["patients"])

@router.post("/", status_code=201)
async def post_patient(background_task: BackgroundTasks, data: dict = Depends(parse_form_data), db=Depends(get_db)):
    patient = PatientCreate(**data)
    image = data["image"]
    patient = create_patient(patient.name, patient.email_address, patient.phone_number, image, db)
    handle_notifications(patient, background_task)
    return patient