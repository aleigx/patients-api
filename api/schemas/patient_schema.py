from pydantic import BaseModel, Field, field_validator
from fastapi import Form, UploadFile, File
from api.exceptions.invalid_input_exception import InvalidInputException


class PatientCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=64)
    email_address: str = Field(..., min_length=3, max_length=64)
    phone_number: str = Field(..., min_length=3, max_length=15)
    
    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        if not value.isdigit():
            raise InvalidInputException("Phone number must be valid.")
        return value

    @field_validator("email_address")
    def validate_email_address(cls, value):
        if "@" not in value:
            raise InvalidInputException("Email address must be valid.")
        return value


async def parse_form_data(
    name: str = Form(...),
    email_address: str = Form(...),
    phone_number: str = Form(...),
    image: UploadFile = File(...),
):
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise InvalidInputException("Image file must be JPEG or PNG format.")
    content = await image.read()
    max_size = 5 * 1024 * 1024  # 5MB
    if len(content) > max_size:
        raise InvalidInputException("Image file size must be less than 5MB.")
    
    return {
        "name": name,
        "email_address": email_address,
        "phone_number": phone_number,
        "image": image
    }
