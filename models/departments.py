from sqlalchemy import Column, Integer, String
from core.database import Base


class DepartmentMaster(Base):
    __tablename__ = "department_master"

    id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String(100), nullable=True)