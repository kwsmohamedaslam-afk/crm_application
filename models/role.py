from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base


class RoleMaster(Base):
    __tablename__ = "role_master"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(100), nullable=False)

    # Relationships
    permissions = relationship(
        "RolePermission",
        back_populates="role",
        cascade="all, delete-orphan"
    )