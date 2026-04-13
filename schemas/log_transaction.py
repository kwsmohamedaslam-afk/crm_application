from typing import Optional
from pydantic import BaseModel


class LogCreate(BaseModel):
    date_time: Optional[str] = None
    events: Optional[str] = None
    user_id: Optional[str] = None


class LogOut(BaseModel):
    id: int
    date_time: Optional[str]
    events: Optional[str]
    user_id: Optional[str]

    model_config = {"from_attributes": True}
