from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_id = Column(
        Integer,
        ForeignKey("role_master.id", ondelete="CASCADE"),  # ✅ FIXED
        primary_key=True
    )

    action_id = Column(
        Integer,
        ForeignKey("actions.id", ondelete="CASCADE"),
        primary_key=True
    )

    # Relationships
    role = relationship(
        "RoleMaster",  # ✅ FIXED
        back_populates="permissions"
    )

    action = relationship(
        "Action",
        back_populates="role_permissions"
    )