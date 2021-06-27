from sqlalchemy import Column, Integer, Boolean, Float
from .database import Base

# Create model for database
class User(Base):
    __tablename__ = 'user'

    _id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    plot_mode = Column(Boolean, default=True)
    digits = Column(Integer, default=6)
    alpha = Column(Float, default=0.05)