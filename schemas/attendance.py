from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class AttendanceResponse(BaseModel):
    id: int
    attendance_date: date
    check_in: Optional[datetime]
    check_out: Optional[datetime]
    total_work_minutes: int
    overtime_minutes: int
    status: Optional[int]

    class Config:
        from_attributes = True