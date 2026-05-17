from pydantic import BaseModel

class ViolationType(BaseModel):
    violation_id: str
    violation_type: str
    
    def __init__(self, *args, **kwargs):
        if args:
            keys = ["violation_id", "violation_type"]
            kwargs.update(zip(keys, args))
        super().__init__(**kwargs)

    def __str__(self):
        return f"ViolationType(violation_id={self.violation_id}, violation_type='{self.violation_type}')"
    
    def get_tuple(self):
        return (self.violation_id, self.violation_type)
    
    @staticmethod
    def get_header():
        return ("Violation ID", "Violation Type")
    
    def serialize(self):
        return self.model_dump() if hasattr(self, 'model_dump') else self.dict()