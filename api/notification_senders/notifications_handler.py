from api.notification_senders.email_sender import EmailSender
from fastapi import BackgroundTasks
from api.models.patient_model import Patient

def get_senders():
    return [EmailSender()]

def handle_notifications(patient: Patient, background_task: BackgroundTasks):
    notification_senders = get_senders()
    for sender in notification_senders:
        background_task.add_task(sender.send_notification, patient, f"Thank you for registering, {patient.name}!")