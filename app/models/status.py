from sqlalchemy import Column, Integer, String, Boolean,DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, index=True)
    bottle1 = Column(String)
    bottle2 = Column(String)
    bottle3 = Column(String)
    bottle4 = Column(String)
    created_at=Column(DateTime)