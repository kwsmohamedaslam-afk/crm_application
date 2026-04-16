from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from services.attendance_service import AttendanceService
from core.security import get_current_user

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/login")
def login(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return AttendanceService.login(db, current_user.id)


@router.post("/break-start")
def break_start(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    AttendanceService.break_start(db, current_user.id)
    return {"message": "Break started"}


@router.post("/break-end")
def break_end(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    AttendanceService.break_end(db, current_user.id)
    return {"message": "Break ended"}


@router.post("/idle-start")
def idle_start(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    AttendanceService.idle_start(db, current_user.id)
    return {"message": "Idle started"}


@router.post("/logout")
def logout(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    AttendanceService.logout(db, current_user.id)
    return {"message": "Logged out"}