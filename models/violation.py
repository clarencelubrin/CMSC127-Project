from pydantic import BaseModel
from datetime import date as Date
from models.violation_type import ViolationType

class Violation(BaseModel):
    violation_id: int
    date: Date
    location: str
    corresponding_fine_amount: float
    apprehending_officer: str
    violation_status: str
    license_no: str
    plate_no: str
    violation_types: list[ViolationType] | None = [] # List of ViolationType objects, can be empty or null

    def __init__(self, 
        *args,
        **kwargs
    ):
        if args:
            keys = [
                "violation_id", "date", "location", "corresponding_fine_amount", 
                "apprehending_officer", "violation_status", "license_no", "plate_no"
            ]
            kwargs.update(zip(keys, args))
        
        super().__init__(**kwargs)

    def __str__(self):
        return f"Violation(violation_id={self.violation_id}, date={self.date}, location='{self.location}', corresponding_fine_amount={self.corresponding_fine_amount}, apprehending_officer='{self.apprehending_officer}', violation_status='{self.violation_status}', license_no={self.license_no}, plate_no='{self.plate_no}'. violation_types={[vt.serialize() for vt in self.violation_types]})"
    
    def set_violation_types(self, violation_types):
        self.violation_types = violation_types
        
    def get_tuple(self):
        return (self.violation_id, self.date, self.location, self.corresponding_fine_amount, self.apprehending_officer, self.violation_status, self.license_no, self.plate_no)

    def get_tuple_with_types(self):
        return (self.violation_id, self.date, self.location, self.corresponding_fine_amount, self.apprehending_officer, self.violation_status, self.license_no, self.plate_no, ", ".join([vt.violation_type for vt in self.violation_types]))
    
    @staticmethod
    def get_headers():
        return ("Violation ID", "Date", "Location", "Corresponding Fine Amount", "Apprehending Officer", "Violation Status", "License No", "Plate No", "Violation Types")
    
    
    def serialize(self):
        data = self.model_dump() if hasattr(self, 'model_dump') else self.dict()
        # Convert date object to string for JSON serialization
        if data.get('date'):
            data['date'] = data['date'].isoformat()
        return data