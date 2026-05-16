from pydantic import BaseModel
from datetime import date as Date
from typing import Any

class Driver(BaseModel):
    license_no: str
    full_name: str
    license_type: str
    license_status: str
    address: str
    sex: str
    date_of_birth: Date
    # registration_no: int | None # Can be null if not registered yet

    def __init__(self, *args, **kwargs):
        if args:
            # Map the database row (tuple) to field names from schema.sql
            keys = [
                "license_no", "full_name", "license_type", "license_status", 
                "address", "sex", "date_of_birth"
            ]
            kwargs.update(zip(keys, args))
        super().__init__(**kwargs)

    def serialize(self):
        data = self.model_dump() if hasattr(self, 'model_dump') else self.dict()
        # Convert date object to string for JSON serialization
        if data.get('date_of_birth'):
            data['date_of_birth'] = data['date_of_birth'].isoformat()
        return data
    @staticmethod
    def get_headers():
        return ("License No.", "Full Name", "Type", "Status", "Address", "Sex", "Birth Date")
    
    def get_tuple(self):
        return (
            self.license_no, self.full_name, self.license_type, 
            self.license_status, self.address, self.sex, 
            self.date_of_birth
        )