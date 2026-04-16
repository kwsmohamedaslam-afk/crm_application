from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status
from fastapi.params import File
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user, hash_password
from models.departments import DepartmentMaster
from models.role import RoleMaster
from models.user import UserMaster
from schemas.user import UserCreate, UserUpdate, UserOut
from services.file_service import FileService
from utils.logger import log_event

router = APIRouter(prefix="/api/users", tags=["Users"])


# ─────────────────────────────────────────────────────────────
# CREATE USER
# ─────────────────────────────────────────────────────────────
# @router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
# def create_user(payload: UserCreate, db: Session = Depends(get_db)):

#     # ✅ Unique checks
#     if db.query(UserMaster).filter(UserMaster.username == payload.username).first():
#         raise HTTPException(409, "Username already exists")

#     if db.query(UserMaster).filter(UserMaster.email == payload.email).first():
#         raise HTTPException(409, "Email already registered")

#     # ✅ Auto user number
#     user_no = f"USR{int(datetime.utcnow().timestamp())}"

#     user = UserMaster(
#         user_no=user_no,
#         username=payload.username,
#         email=payload.email,
#         password=hash_password(payload.password),

#         roleid=payload.roleid,
#         phone_no=payload.phone_no,

#         first_name=payload.first_name,
#         last_name=payload.last_name,
#         surname=payload.surname,
#         date_of_birth=payload.date_of_birth,

#         passport_no=payload.passport_no,
#         passport_file=payload.passport_file,
#         profile_image=payload.profile_image,

#         address=payload.address,
#         joining_date=payload.joining_date,

#         is_active=True,
#         failed_attempts=0,
#     )

#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     log_event(db, str(user.id), f"New user registered: '{user.username}'")
#     return user





def parse_date(date_str: str):
    """Safely parse date string (YYYY-MM-DD)"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(400, f"Invalid date format: {date_str}. Use YYYY-MM-DD")

# @router.post("", status_code=status.HTTP_201_CREATED)   # Without slash
@router.post("/", status_code=status.HTTP_201_CREATED)  # With slash
async def create_user(
    # Form fields (all required or optional)
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    
    # Optional fields
    roleid: Optional[int] = Form(None),
    phone_no: Optional[str] = Form(None),
    
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    # surname: Optional[str] = Form(None),
    date_of_birth: Optional[str] = Form(None),
    
    # passport_no: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    joining_date: Optional[str] = Form(None),
    monthly_salary: Optional[float] = Form(None),
    
    # File uploads
    profile_image: Optional[UploadFile] = File(None),
    passport_file: Optional[UploadFile] = File(None),
    department_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    # Validate required fields
    if not username or not email or not password:
        raise HTTPException(400, "username, email, and password are required")
    
    # Unique checks
    if db.query(UserMaster).filter(UserMaster.username == username).first():
        raise HTTPException(status_code=409, detail="Username already exists")
    
    if db.query(UserMaster).filter(UserMaster.email == email).first():
        raise HTTPException(status_code=409, detail="Email already exists")
    
    # Role check
    if roleid:
        role = db.query(RoleMaster).filter(RoleMaster.id == roleid).first()
        if not role:
            raise HTTPException(400, "Invalid role ID")
        
    # Department check
    if department_id:
        department = db.query(DepartmentMaster).filter(
        DepartmentMaster.id == department_id
    ).first()

    if not department:
        raise HTTPException(400, "Invalid department ID")    
    
    # File upload
    profile_path = None
    passport_path = None
    
    try:
        if profile_image and profile_image.filename:
            profile_path = FileService.upload_profile_image(profile_image)
        
        if passport_file and passport_file.filename:
            passport_path = FileService.upload_passport(passport_file)
    except Exception as e:
        raise HTTPException(500, f"File upload failed: {str(e)}")
    
    # Parse dates
    dob = parse_date(date_of_birth) if date_of_birth else None
    join_date = parse_date(joining_date) if joining_date else None
    
    # Create user
    user = UserMaster(
        user_no=f"USR{int(datetime.utcnow().timestamp())}",
        username=username,
        email=email,
        password=hash_password(password),
        roleid=roleid,
        phone_no=phone_no,
        first_name=first_name,
        last_name=last_name,
        # surname=surname,
        date_of_birth=dob,
        # passport_no=passport_no,
        passport_file=passport_path,
        profile_image=profile_path,
        address=address,
        monthly_salary=monthly_salary,
        joining_date=join_date,
        status=True,
        failed_attempts=0,
        department_id=department_id
    )
    
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"User creation failed: {str(e)}")
    
    return user
# ─────────────────────────────────────────────────────────────
# LIST USERS
# ─────────────────────────────────────────────────────────────
# @router.get("/", response_model=List[UserOut])
# def list_users(
#     db: Session = Depends(get_db),
#     current_user: UserMaster = Depends(get_current_user),
# ):
#     return db.query(UserMaster).all()



@router.get("/", response_model=List[UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user: UserMaster = Depends(get_current_user),
):
    try:
        users = db.query(UserMaster).all()
        return users

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@router.get("/active", response_model=List[UserOut])
def get_active_users(
    db: Session = Depends(get_db),
    current_user: UserMaster = Depends(get_current_user),
):
    try:
        users = db.query(UserMaster).filter(
            UserMaster.is_active == True
        ).all()

        return users

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

# ─────────────────────────────────────────────────────────────
# GET USER
# ─────────────────────────────────────────────────────────────
@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserMaster = Depends(get_current_user),
):
    user = db.query(UserMaster).filter(UserMaster.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    return user


# ─────────────────────────────────────────────────────────────
# UPDATE USER
# ─────────────────────────────────────────────────────────────
@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int,
    # Form fields (all optional for update)
    username: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    
    # Optional fields
    roleid: Optional[int] = Form(None),
    phone_no: Optional[str] = Form(None),
    
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    # surname: Optional[str] = Form(None),
    date_of_birth: Optional[str] = Form(None),
    
    # passport_no: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    joining_date: Optional[str] = Form(None),
    
    # File uploads
    profile_image: Optional[UploadFile] = File(None),
    passport_file: Optional[UploadFile] = File(None),
    department_id: Optional[int] = Form(None),
    monthly_salary: Optional[float] = Form(None),
    db: Session = Depends(get_db),
    current_user: UserMaster = Depends(get_current_user)
):
    # Check if user exists
    user = db.query(UserMaster).filter(UserMaster.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Username uniqueness check (if being updated)
    if username is not None and username != user.username:
        existing = db.query(UserMaster).filter(
            UserMaster.username == username,
            UserMaster.id != user_id
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail="Username already exists")
        user.username = username
    
    # Email uniqueness check (if being updated)
    if email is not None and email != user.email:
        existing = db.query(UserMaster).filter(
            UserMaster.email == email,
            UserMaster.id != user_id
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail="Email already exists")
        user.email = email
    
    # Role check (if being updated)
    if roleid is not None:
        role = db.query(DepartmentMaster).filter(DepartmentMaster.id == roleid).first()
        if not role:
            raise HTTPException(status_code=400, detail="Invalid role ID")
        user.roleid = roleid
    if department_id is not None:
        department = db.query(DepartmentMaster).filter(DepartmentMaster.id == department_id).first()
        if not department:
            raise HTTPException(status_code=400, detail="Invalid department ID")
        user.department_id = department_id
    
    # Password update (if provided)
    if password is not None:
        user.password = hash_password(password)
    
    # File upload handling (only if new files are provided)
    try:
        if profile_image and profile_image.filename:
            # Optionally delete old file
            if user.profile_image:
                FileService.delete_file(user.profile_image)
            user.profile_image = FileService.upload_profile_image(profile_image)
        
        if passport_file and passport_file.filename:
            # Optionally delete old file
            if user.passport_file:
                FileService.delete_file(user.passport_file)
            user.passport_file = FileService.upload_passport(passport_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
    
    # Update simple fields (only if provided)
    if phone_no is not None:
        user.phone_no = phone_no
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    # if surname is not None:
    #     user.surname = surname
    # if passport_no is not None:
    #     user.passport_no = passport_no
    if monthly_salary is not None:
        user.monthly_salary = monthly_salary

    if address is not None:
        user.address = address
    
    # Date fields (parse if provided)
    if date_of_birth is not None:
        user.date_of_birth = parse_date(date_of_birth) if date_of_birth else None
    if joining_date is not None:
        user.joining_date = parse_date(joining_date) if joining_date else None
    
    # Commit changes
    try:
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"User update failed: {str(e)}")
    
    # Log the update
    log_event(db, str(current_user.id), f"Updated user id={user_id}")
    
    return user


# ─────────────────────────────────────────────────────────────
# DELETE USER (SOFT DELETE RECOMMENDED)
# ─────────────────────────────────────────────────────────────
@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserMaster = Depends(get_current_user),
):

    user = db.query(UserMaster).filter(UserMaster.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    # 🔥 Better: soft delete instead of hard delete
    user.is_active = False

    db.commit()

    log_event(db, str(current_user.id), f"Deactivated user id={user_id}")
    return {"message": f"User {user_id} deactivated successfully"}