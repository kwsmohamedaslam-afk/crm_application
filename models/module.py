from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)

    department_id = Column(
        Integer,
        ForeignKey("department_master.id", ondelete="CASCADE"),  # ✅ FIXED
        nullable=False
    )

    name = Column(String(100), nullable=False)

    # Relationships
    department = relationship(
        "DepartmentMaster",  # ✅ FIXED
        back_populates="modules"
    )

    actions = relationship(
        "Action",
        back_populates="module",
        cascade="all, delete-orphan"
    )