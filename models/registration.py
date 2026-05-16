from pydantic import BaseModel
from datetime import date as Date

class Registration(BaseModel):
    registration_no: int
    registration_date: Date
    expiration_date: Date
    registration_status: str
    license_no: str | None # Can be null if not connected to a driver
    plate_no: str | None # Can be null if not connected to a vehicle

    def __init__(self, 
        *args,
        **kwargs
    ):
        if args:
            keys = ["registration_no", "registration_date", "expiration_date", "registration_status", "license_no", "plate_no"]
            kwargs.update(zip(keys, args))
        super().__init__(**kwargs)

    def __str__(self):
        return f"Registration(registration_no={self.registration_no}, registration_date={self.registration_date}, expiration_date={self.expiration_date}, registration_status='{self.registration_status}')"    

    @staticmethod
    def get_headers():
        return ("Registration No", "Registration Date", "Expiration Date", "Registration Status", "License No", "Plate No")
    
    def get_tuple(self):
        return (self.registration_no, self.registration_date, self.expiration_date, self.registration_status, self.license_no, self.plate_no)
    
    def serialize(self):
        data = self.model_dump() if hasattr(self, 'model_dump') else self.dict()
        # Convert date object to string for JSON serialization
        if data.get('registration_date'):
            data['registration_date'] = data['registration_date'].isoformat()
        if data.get('expiration_date'):
            data['expiration_date'] = data['expiration_date'].isoformat()

        data['license_no'] = self.license_no
        data['plate_no'] = self.plate_no

        return data