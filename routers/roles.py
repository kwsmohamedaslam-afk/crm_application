from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user
from models.role import RoleMaster
from models.user import UserMaster
from schemas.role import RoleCreate, RoleUpdate, RoleOut
from utils.logger import log_event

router = APIRouter(prefix="/api/roles", tags=["Roles"])


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

@router.post("/", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
def create_role(
    payload: RoleCreate,
    db: Session = Depends(get_db),
    user_id: int = Header(None)  # 👈 only for logging
):
    role = RoleMaster(role_name=payload.role_name)
    db.add(role)
    db.commit()
    db.refresh(role)

    log_event(
        db,
        str(user_id) if user_id else "anonymous",
        f"Created role '{role.role_name}' (id={role.id})"
    )

    return role


@router.get("/", response_model=List[RoleOut], summary="List all roles")
def list_roles(
    db: Session = Depends(get_db),
    current_user: UserMaster = Depends(get_current_user),
):
    """Retrieve all roles."""
    return db.query(RoleMaster).all()


@router.get("/{role_id}", response_model=RoleOut, summary="Get a role by ID")
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: UserMaster = Depends(get_current_user),
):
    """Retrieve a single role by its primary key."""
    role = db.query(RoleMaster).filter(RoleMaster.id == role_id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return role


@router.put("/{role_id}", response_model=RoleOut, summary="Update a role")
def update_role(
    role_id: int,
    payload: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: UserMaster = Depends(get_current_user),
):
    """Update fields of an existing role."""
    role = db.query(RoleMaster).filter(RoleMaster.id == role_id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    if payload.role_name is not None:
        role.role_name = payload.role_name

    db.commit()
    db.refresh(role)
    log_event(db, str(current_user.id), f"Updated role id={role_id}")
    return role


@router.delete("/{role_id}", status_code=status.HTTP_200_OK, summary="Delete a role")
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: UserMaster = Depends(get_current_user),
):
    """Delete a role by ID."""
    role = db.query(RoleMaster).filter(RoleMaster.id == role_id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    db.delete(role)
    db.commit()
    log_event(db, str(current_user.id), f"Deleted role id={role_id}")
    return {"message": f"Role {role_id} deleted successfully"}
