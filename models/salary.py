from sqlalchemy import Column, Integer, Float, Enum, ForeignKey
from core.database import Base


class SalaryStructure(Base):
    __tablename__ = "salary_structure"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_master.id"), nullable=False)

    salary_type = Column(Enum("MONTHLY", "DAILY", "HOURLY"), nullable=False)

    base_salary = Column(Float, nullable=True)
    per_day_salary = Column(Float, nullable=True)
    per_hour_salary = Column(Float, nullable=True)

    overtime_rate = Column(Float, default=0)