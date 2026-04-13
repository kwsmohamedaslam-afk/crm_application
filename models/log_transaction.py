from sqlalchemy import Column, Integer, String, Text
from core.database import Base


class LogTransaction(Base):
    __tablename__ = "log_transaction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_time = Column(String(45), nullable=True)
    events = Column(Text, nullable=True)
    user_id = Column(String(45), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_action = Column(Text, nullable=True)