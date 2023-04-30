from sqlalchemy import Column, Integer, String, Boolean,DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"

    idorder = Column(Integer, primary_key=True, index=True)
    drink = Column(String)
    user = Column(String)
    created_at = Column(DateTime)