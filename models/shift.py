from sqlalchemy import Column, BigInteger, String, Time, Boolean, DECIMAL, Integer, JSON, TIMESTAMP, text
from core.database import Base


class ShiftMaster(Base):
    __tablename__ = "shift_master"

    shift_id = Column(BigInteger, primary_key=True, index=True)

    shift_name = Column(String(100), nullable=False)

    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    total_daily_work_hours = Column(DECIMAL(5, 2), nullable=True)
    total_weekly_work_hours = Column(DECIMAL(5, 2), nullable=True)

    working_days_per_week = Column(Integer, nullable=True)

    weekly_off = Column(JSON, nullable=True)

    is_night_shift = Column(Boolean, default=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )