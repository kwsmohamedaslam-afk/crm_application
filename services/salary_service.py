from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.salary import SalaryStructure
from models.attendance import Attendance


def calculate_salary(db: Session, user_id: int):
    salary = db.query(SalaryStructure).filter(
        SalaryStructure.user_id == user_id
    ).first()

    if not salary:
        raise HTTPException(status_code=404, detail="Salary structure not found")

    attendances = db.query(Attendance).filter(
        Attendance.user_id == user_id
    ).all()

    total_minutes = sum(a.total_work_minutes or 0 for a in attendances)
    overtime_minutes = sum(a.overtime_minutes or 0 for a in attendances)

    total_hours = total_minutes / 60
    overtime_hours = overtime_minutes / 60

    total_salary = 0

    # 🔹 HOURLY
    if salary.salary_type == "HOURLY":
        base = total_hours * (salary.per_hour_salary or 0)
        overtime = overtime_hours * (salary.overtime_rate or 0)
        total_salary = base + overtime

    # 🔹 DAILY
    elif salary.salary_type == "DAILY":
        present_days = len([a for a in attendances if a.status == 1])
        total_salary = present_days * (salary.per_day_salary or 0)

    # 🔹 MONTHLY
    elif salary.salary_type == "MONTHLY":
        total_salary = salary.base_salary or 0

    return {
        "total_work_hours": round(total_hours, 2),
        "overtime_hours": round(overtime_hours, 2),
        "salary": round(total_salary, 2)
    }