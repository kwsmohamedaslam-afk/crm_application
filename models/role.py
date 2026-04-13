from sqlalchemy import Column, Integer, String
from core.database import Base


class RoleMaster(Base):
    __tablename__ = "role_master"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(100), nullable=True)
