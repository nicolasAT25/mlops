from .database import Base
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from sqlalchemy.sql.expression import text

class NewData(Base):
    __tablename__ = "new_data"
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    prediction = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False) 

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    prediction = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False) 