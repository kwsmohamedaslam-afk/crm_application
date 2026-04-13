from typing import Optional
from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    department_name: str


class DepartmentUpdate(BaseModel):
    department_name: Optional[str] = None


class DepartmentOut(BaseModel):
    id: int
    department_name: Optional[str]

    model_config = {"from_attributes": True}
