from datetime import datetime, date
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.attendance import Attendance


def check_in(db: Session, user_id: int):
    today = date.today()

    attendance = db.query(Attendance).filter(
        Attendance.user_id == user_id,
        Attendance.attendance_date == today
    ).first()

    if attendance and attendance.check_in:
        raise HTTPException(status_code=400, detail="Already checked in")

    if not attendance:
        attendance = Attendance(
            user_id=user_id,
            attendance_date=today
        )

    attendance.check_in = datetime.utcnow()
    attendance.status = 1  # Present

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return attendance


def check_out(db: Session, user_id: int):
    today = date.today()

    attendance = db.query(Attendance).filter(
        Attendance.user_id == user_id,
        Attendance.attendance_date == today
    ).first()

    if not attendance or not attendance.check_in:
        raise HTTPException(status_code=400, detail="Check-in required first")

    if attendance.check_out:
        raise HTTPException(status_code=400, detail="Already checked out")

    # check active break before checkout
    active_break = db.query(AttendanceBreak).filter(
        AttendanceBreak.attendance_id == attendance.id,
        AttendanceBreak.break_end == None
    ).first()

    if active_break:
        raise HTTPException(status_code=400, detail="End break before checkout")

    attendance.check_out = datetime.utcnow()

    total_minutes = int((attendance.check_out - attendance.check_in).total_seconds() / 60)

    break_minutes = sum(b.break_minutes for b in attendance.breaks)

    attendance.total_break_minutes = break_minutes
    attendance.total_work_minutes = total_minutes - break_minutes

    # overtime
    if attendance.total_work_minutes > 480:
        attendance.overtime_minutes = attendance.total_work_minutes - 480

    db.commit()
    db.refresh(attendance)

    return attendance


def get_my_attendance(db: Session, user_id: int):
    return db.query(Attendance).filter(
        Attendance.user_id == user_id
    ).order_by(Attendance.attendance_date.desc()).all()


def get_all_attendance(db: Session):
    return db.query(Attendance).all()

from models.attendance_break import AttendanceBreak


def start_break(db: Session, user_id: int):
    today = date.today()

    attendance = db.query(Attendance).filter(
        Attendance.user_id == user_id,
        Attendance.attendance_date == today
    ).first()

    if not attendance or not attendance.check_in:
        raise HTTPException(status_code=400, detail="Check-in required before break")

    if attendance.check_out:
        raise HTTPException(status_code=400, detail="Cannot start break after check-out")

    # check active break
    active_break = db.query(AttendanceBreak).filter(
        AttendanceBreak.attendance_id == attendance.id,
        AttendanceBreak.break_end == None
    ).first()

    if active_break:
        raise HTTPException(status_code=400, detail="Break already active")

    new_break = AttendanceBreak(
        attendance_id=attendance.id,
        break_start=datetime.utcnow()
    )

    db.add(new_break)
    db.commit()

    return new_break

def end_break(db: Session, user_id: int):
    today = date.today()

    attendance = db.query(Attendance).filter(
        Attendance.user_id == user_id,
        Attendance.attendance_date == today
    ).first()

    if not attendance:
        raise HTTPException(status_code=400, detail="Attendance not found")

    active_break = db.query(AttendanceBreak).filter(
        AttendanceBreak.attendance_id == attendance.id,
        AttendanceBreak.break_end == None
    ).first()

    if not active_break:
        raise HTTPException(status_code=400, detail="No active break")

    active_break.break_end = datetime.utcnow()

    minutes = int((active_break.break_end - active_break.break_start).total_seconds() / 60)
    active_break.break_minutes = minutes

    # update total break time
    total_break = sum(b.break_minutes for b in attendance.breaks if b.break_minutes)
    attendance.total_break_minutes = total_break

    db.commit()

    return active_break