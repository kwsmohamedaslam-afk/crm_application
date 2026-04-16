from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base


class DepartmentMaster(Base):
    __tablename__ = "department_master"

    id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String(100), nullable=False)

    # Relationships
    modules = relationship(
        "Module",
        back_populates="department",
        cascade="all, delete-orphan"
    )