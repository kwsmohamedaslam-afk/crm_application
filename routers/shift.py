from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from models.shift import ShiftMaster
from schemas.shift import ShiftCreate, ShiftResponse, calculate_hours

router = APIRouter(prefix="/api/shifts", tags=["Shifts"])


# ✅ CREATE SHIFT
@router.post("/", response_model=ShiftResponse)
def create_shift(payload: ShiftCreate, db: Session = Depends(get_db)):
    try:
        # 🔥 Calculate daily hours
        daily_hours = calculate_hours(payload.start_time, payload.end_time)

        # 🔥 Weekly hours
        weekly_hours = daily_hours * payload.working_days_per_week

        # 🔥 Night shift check
        is_night = payload.end_time <= payload.start_time

        shift = ShiftMaster(
            shift_name=payload.shift_name,
            start_time=payload.start_time,
            end_time=payload.end_time,
            total_daily_work_hours=daily_hours,
            total_weekly_work_hours=weekly_hours,
            working_days_per_week=payload.working_days_per_week,
            weekly_off=payload.weekly_off,
            is_night_shift=is_night,
            is_active=payload.is_active,
        )

        db.add(shift)
        db.commit()
        db.refresh(shift)

        return shift

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ✅ GET ALL SHIFTS
@router.get("/", response_model=List[ShiftResponse])
def get_shifts(db: Session = Depends(get_db)):
    return db.query(ShiftMaster).all()


# ✅ GET SINGLE SHIFT
@router.get("/{shift_id}", response_model=ShiftResponse)
def get_shift(shift_id: int, db: Session = Depends(get_db)):
    shift = db.query(ShiftMaster).filter(ShiftMaster.shift_id == shift_id).first()

    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")

    return shift


# ✅ UPDATE SHIFT
@router.put("/{shift_id}", response_model=ShiftResponse)
def update_shift(shift_id: int, payload: ShiftCreate, db: Session = Depends(get_db)):
    shift = db.query(ShiftMaster).filter(ShiftMaster.shift_id == shift_id).first()

    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")

    # 🔥 Recalculate
    daily_hours = calculate_hours(payload.start_time, payload.end_time)
    weekly_hours = daily_hours * payload.working_days_per_week
    is_night = payload.end_time <= payload.start_time

    shift.shift_name = payload.shift_name
    shift.start_time = payload.start_time
    shift.end_time = payload.end_time
    shift.total_daily_work_hours = daily_hours
    shift.total_weekly_work_hours = weekly_hours
    shift.working_days_per_week = payload.working_days_per_week
    shift.weekly_off = payload.weekly_off
    shift.is_night_shift = is_night
    shift.is_active = payload.is_active

    db.commit()
    db.refresh(shift)

    return shift


# ✅ SOFT DELETE (Deactivate)
@router.delete("/{shift_id}")
def delete_shift(shift_id: int, db: Session = Depends(get_db)):
    shift = db.query(ShiftMaster).filter(ShiftMaster.shift_id == shift_id).first()

    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")

    shift.is_active = False
    db.commit()

    return {"message": "Shift deactivated successfully"}