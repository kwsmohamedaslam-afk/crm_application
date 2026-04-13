from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user

from services import salary_service

router = APIRouter(prefix="/salary", tags=["Salary"])


def response(success: bool, message: str, data=None):
    return {
        "success": success,
        "message": message,
        "data": data
    }


# 🔹 USER SALARY
@router.get("/me")
def my_salary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    data = salary_service.calculate_salary(db, current_user.id)
    return response(True, "Salary calculated", data)


# 🔹 ADMIN VIEW ANY USER SALARY
@router.get("/user/{user_id}")
def user_salary(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.roleid != 1:
        return response(False, "Unauthorized")

    data = salary_service.calculate_salary(db, user_id)
    return response(True, "Salary fetched", data)