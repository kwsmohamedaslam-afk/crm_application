from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime


class AttendanceEvent(Base):
    __tablename__ = "attendance_events"

    id = Column(Integer, primary_key=True, index=True)
    attendance_id = Column(Integer, ForeignKey("attendance.id"), nullable=False)

    event_type = Column(String(50), nullable=False)  
    # BREAK_START, BREAK_END, IDLE_START, IDLE_END

    event_time = Column(DateTime, default=datetime.utcnow)

    attendance = relationship("Attendance", back_populates="events")