from pydantic import BaseModel

# Schema for creating fee records
class FeeCreate(BaseModel):
    student_id: int
    amount: float
    paid: int = 0  # 0 = not paid, 1 = paid

# Schema for returning fee records
class FeeOut(BaseModel):
    id: int
    student_id: int
    amount: float
    paid: int

    class Config:
        from_attributes = True