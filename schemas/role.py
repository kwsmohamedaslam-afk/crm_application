from typing import Optional
from pydantic import BaseModel


class RoleCreate(BaseModel):
    role_name: str


class RoleUpdate(BaseModel):
    role_name: Optional[str] = None


class RoleOut(BaseModel):
    id: int
    role_name: Optional[str]

    model_config = {"from_attributes": True}
