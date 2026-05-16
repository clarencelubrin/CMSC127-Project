from pydantic import BaseModel

class Vehicle(BaseModel):
    plate_no: str
    engine_no: str
    chassis_no: str
    vehicle_type: str
    color: str
    year: int
    model: str
    make: str
    # registration_no: int | None # Can be null if not registered yet
    license_no: str | None # Can be null if not registered yet

    def __init__(self, *args, **kwargs):
        # If args are passed (like from a DB row tuple), map them to keys
        if args:
            keys = [
                'plate_no', 'engine_no', 'chassis_no', 'vehicle_type', 
                'color', 'year', 'model', 'make', 'license_no'
            ]
            kwargs.update(zip(keys, args))
        
        # Initialize the Pydantic BaseModel correctly
        super().__init__(**kwargs)

    def __str__(self):
        return f"Vehicle(plate_no='{self.plate_no}', model='{self.model}', make='{self.make}')"
    
    def get_tuple(self):
        # Returns a tuple in the exact order required by the schema
        return (
            self.plate_no, self.engine_no, self.chassis_no, self.vehicle_type, 
            self.color, self.year, self.model, self.make, 
            self.license_no
        )
    
    @staticmethod
    def get_headers():
        return ("Plate No", "Engine No", "Chassis No", "Vehicle Type", "Color", "Year", "Model", "Make", "License No")

    def serialize(self):
        return self.model_dump() if hasattr(self, 'model_dump') else self.dict()