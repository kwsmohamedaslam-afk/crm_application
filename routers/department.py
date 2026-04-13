from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user
from models import role
from models.departments import DepartmentMaster
from models.role import RoleMaster
from models.user import UserMaster
from schemas.department import DepartmentCreate, DepartmentOut, DepartmentUpdate
from schemas.role import RoleCreate, RoleUpdate, RoleOut
from utils.logger import log_event

router = APIRouter(prefix="/api/departments", tags=["Departments"])


# @router.post("/", response_model=RoleOut, status_code=status.HTTP_201_CREATED, summary="Create a role")
# def create_role(
#     payload: RoleCreate,
#     db: Session = Depends(get_db),
#     current_user: UserMaster = Depends(get_current_user),
# ):
#     """Create a new role. Requires authentication."""
#     role = RoleMaster(role_name=payload.role_name)
#     db.add(role)
#     db.commit()
#     db.refresh(role)
#     log_event(db, str(current_user.id), f"Created role '{role.role_name}' (id={role.id})")
#     return role

from fastapi import Header

@router.post("/", response_model=DepartmentOut, status_code=status.HTTP_201_CREATED)
def create_department(
    payload: DepartmentCreate,
    db: Session = Depends(get_db),
    user_id: int = Header(None)  # 👈 only for logging
):
    department = DepartmentMaster(department_name=payload.department_name)
    db.add(department)
    db.commit()
    db.refresh(department)

    log_event(
        db,
        str(user_id) if user_id else "anonymous",
        f"Created department '{department.department_name}' (id={department.id})"
    )

    return department


@router.get("/", response_model=List[DepartmentOut], summary="List all departments")
def list_departments(
    db: Session = Depends(get_db),
    current_user: UserMaster = Depends(get_current_user),
):
    """Retrieve all departments."""
    return db.query(DepartmentMaster).all()


@router.get("/{department_id}", response_model=DepartmentOut, summary="Get a department by ID")
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: UserMaster = Depends(get_current_user),
):
    """Retrieve a single department by its primary key."""
    department = db.query(DepartmentMaster).filter(DepartmentMaster.id == department_id).first()
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    return department   


@router.put("/{department_id}", response_model=DepartmentOut, summary="Update a department")
def update_department(
    department_id: int,
    payload: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: UserMaster = Depends(get_current_user),
):
    """Update fields of an existing department."""
    department = db.query(DepartmentMaster).filter(DepartmentMaster.id == department_id).first()
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    if payload.department_name is not None:
        department.department_name = payload.department_name

    db.commit()
    db.refresh(department)
    log_event(db, str(current_user.id), f"Updated department id={department_id}")
    return department


@router.delete("/{department_id}", status_code=status.HTTP_200_OK, summary="Delete a department")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: UserMaster = Depends(get_current_user),
):
    """Delete a department by ID."""
    department = db.query(DepartmentMaster).filter(DepartmentMaster.id == department_id).first()
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    db.delete(department)
    db.commit()
    log_event(db, str(current_user.id), f"Deleted department id={department_id}")
    return {"message": f"Department {department_id} deleted successfully"}
