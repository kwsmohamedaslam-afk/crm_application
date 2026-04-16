from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)

    module_id = Column(
        Integer,
        ForeignKey("modules.id", ondelete="CASCADE"),
        nullable=False
    )

    name = Column(String(100), nullable=False)

    # Relationships
    module = relationship(
        "Module",
        back_populates="actions"
    )

    role_permissions = relationship(
        "RolePermission",
        back_populates="action",
        cascade="all, delete-orphan"
    )