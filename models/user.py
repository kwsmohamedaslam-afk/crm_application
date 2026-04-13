from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, Boolean, Text
from datetime import datetime

from sqlalchemy.orm import relationship
from core.database import Base


class UserMaster(Base):
    __tablename__ = "user_master"

    # 🔑 Basic Info
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_no = Column(String(50), unique=True, nullable=True)  # employee/user number

    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    # 👤 Personal Info
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    surname = Column(String(100), nullable=True)

    date_of_birth = Column(Date, nullable=True)

    phone_no = Column(String(25), nullable=True)
    address = Column(Text, nullable=True)

    # 🪪 Identity
    passport_no = Column(String(50), nullable=True)

    # 📁 File Upload Paths (store only path, not file)
    passport_file = Column(String(500), nullable=True)
    profile_image = Column(String(500), nullable=True)

    # 🏢 Work Info
    roleid = Column(Integer, nullable=True)
    joining_date = Column(Date, nullable=True)

    # 🔐 Security
    failed_attempts = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    # 🕒 Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    attendances = relationship("Attendance", back_populates="user")

        # ✅ NEW FIELD
    department_id = Column(Integer, ForeignKey("department_master.id"), nullable=True)

    # ✅ RELATIONSHIP
    department = relationship("DepartmentMaster", backref="users")