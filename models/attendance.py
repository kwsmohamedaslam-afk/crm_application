from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from core.database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_master.id"), nullable=False)
    attendance_date = Column(Date, nullable=False)

    check_in = Column(DateTime, nullable=True)
    check_out = Column(DateTime, nullable=True)

    total_work_minutes = Column(Integer, default=0)
    total_break_minutes = Column(Integer, default=0)
    overtime_minutes = Column(Integer, default=0)

    status = Column(Integer, nullable=True)

    # ✅ ADD THIS (MISSING LINE)
    user = relationship("UserMaster", back_populates="attendances")

    # existing
    breaks = relationship(
        "AttendanceBreak",
        back_populates="attendance",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("user_id", "attendance_date", name="unique_user_date"),
    )