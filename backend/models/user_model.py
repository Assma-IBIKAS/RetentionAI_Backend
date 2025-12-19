from backend.database.db import Base
from sqlalchemy import Column, DateTime, Integer, String
from datetime import datetime, timezone

class users(Base):
    __tablename__= "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )