from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    roleid: Optional[int] = None
    phone_no: Optional[str] = None
    user_no: Optional[str]= None

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    # surname: Optional[str] = None

    date_of_birth: Optional[str] = None  # or date

    # passport_no: Optional[str] = None
    passport_file: Optional[str] = None
    profile_image: Optional[str] = None

    address: Optional[str] = None
    joining_date: Optional[str] = None
    monthly_salary: Optional[float] = None
    department_id: Optional[int] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    user_no: Optional[str]=None

    roleid: Optional[int] = None
    phone_no: Optional[str] = None

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    # surname: Optional[str] = None

    date_of_birth: Optional[str] = None

    # passport_no: Optional[str] = None
    passport_file: Optional[str] = None
    profile_image: Optional[str] = None

    address: Optional[str] = None
    joining_date: Optional[str] = None
    monthly_salary: Optional[float] = None
    department_id: Optional[int] = None

    status: Optional[bool] = None


class UserOut(BaseModel):
    id: int
    user_no: Optional[str]

    username: str
    email: str

    roleid: Optional[int]
    phone_no: Optional[str]

    first_name: Optional[str]
    last_name: Optional[str]
    # surname: Optional[str]

    date_of_birth: Optional[date]=None

    # passport_no: Optional[str]
    passport_file: Optional[str]
    profile_image: Optional[str]

    address: Optional[str]
    joining_date: Optional[date] =None
    monthly_salary: Optional[float]
    department_id: Optional[int]
    status: Optional[bool]

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
