from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class AttendanceBreak(Base):
    __tablename__ = "attendance_breaks"

    id = Column(Integer, primary_key=True, index=True)
    attendance_id = Column(Integer, ForeignKey("attendance.id"), nullable=False)

    break_start = Column(DateTime, nullable=False)
    break_end = Column(DateTime, nullable=True)

    break_minutes = Column(Integer, default=0)

    attendance = relationship("Attendance", back_populates="breaks")