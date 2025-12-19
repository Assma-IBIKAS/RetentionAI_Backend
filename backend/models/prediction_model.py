from backend.database.db import Base
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime


class PredictionsHistory(Base):
    __tablename__ = "predictions_history"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    probability = Column(Float)
