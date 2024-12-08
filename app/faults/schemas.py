from datetime import datetime
from pydantic import BaseModel
from pydantic import UUID4


class SFaults(BaseModel):
    id: UUID4
    ip: str
    date: datetime
    body_fault: dict
    code_fault: int
    comment: str

    class Config:
        orm_mode = True
        
class FaultCreate(BaseModel):
    ip: str
    date: datetime
    body_fault: dict
    code_fault: int
    comment: str

    class Config:
        orm_mode = True

class DictValidation(BaseModel):
    value: dict