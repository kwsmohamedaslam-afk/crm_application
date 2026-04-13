from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user

from services import attendance_service
from schemas.attendance import AttendanceResponse

router = APIRouter(prefix="/attendance", tags=["Attendance"])


def response(success: bool, message: str, data=None):
    return {
        "success": success,
        "message": message,
        "data": data
    }


@router.post("/check-in")
def check_in(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    data = attendance_service.check_in(db, current_user.id)
    return response(True, "Checked in successfully", data)


@router.post("/check-out")
def check_out(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    data = attendance_service.check_out(db, current_user.id)
    return response(True, "Checked out successfully", data)


@router.get("/me")
def my_attendance(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    data = attendance_service.get_my_attendance(db, current_user.id)
    return response(True, "My attendance fetched", data)


@router.get("/all")
def all_attendance(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.roleid != 1:  # assume admin = 1
        return response(False, "Unauthorized")

    data = attendance_service.get_all_attendance(db)
    return response(True, "All attendance fetched", data)

@router.post("/break-start")
def break_start(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    data = attendance_service.start_break(db, current_user.id)
    return response(True, "Break started", data)


@router.post("/break-end")
def break_end(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    data = attendance_service.end_break(db, current_user.id)
    return response(True, "Break ended", data)