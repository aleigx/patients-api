from sqlalchemy import Column, Integer, String
from api.db.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email_address = Column(String, unique=True)
    phone_number = Column(String)
    image_path = Column(String)