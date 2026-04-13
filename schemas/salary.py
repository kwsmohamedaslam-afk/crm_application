from pydantic import BaseModel


class SalaryResponse(BaseModel):
    total_work_hours: float
    overtime_hours: float
    salary: float