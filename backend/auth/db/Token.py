from uuid import UUID
from sqlalchemy import Column, Integer, String, DateTime,Boolean
from database import Base
import datetime

class Token(Base):
    __tablename__ = "token"
    user_id = Column(UUID(as_uuid=True))
    refresh_token = Column(String(450),nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)