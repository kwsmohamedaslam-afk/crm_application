from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import time, datetime, timedelta


class ShiftBase(BaseModel):
    shift_name: str
    start_time: time
    end_time: time
    working_days_per_week: int
    weekly_off: Optional[List[str]] = []

    is_active: Optional[bool] = True


class ShiftCreate(ShiftBase):
    pass


class ShiftResponse(ShiftBase):
    shift_id: int
    total_daily_work_hours: Optional[float]
    total_weekly_work_hours: Optional[float]
    is_night_shift: bool

    class Config:
        from_attributes = True


# 🔥 Utility function (important)
def calculate_hours(start: time, end: time) -> float:
    start_dt = datetime.combine(datetime.today(), start)
    end_dt = datetime.combine(datetime.today(), end)

    if end_dt <= start_dt:
        end_dt += timedelta(days=1)

    diff = end_dt - start_dt
    return round(diff.total_seconds() / 3600, 2)