from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_master.id"), nullable=False)

    check_in = Column(DateTime, default=datetime.utcnow)
    check_out = Column(DateTime, nullable=True)

    status = Column(String(50), default="WORKING")

    last_activity_at = Column(DateTime, default=datetime.utcnow)

    total_work_minutes = Column(Integer, default=0)
    total_break_minutes = Column(Integer, default=0)
    total_idle_minutes = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    events = relationship("AttendanceEvent", back_populates="attendance", cascade="all, delete")

    user = relationship("UserMaster", back_populates="attendances") 