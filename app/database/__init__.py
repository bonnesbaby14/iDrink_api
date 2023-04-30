from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:1234@localhost/idrink_db")

Session = sessionmaker(bind=engine)
session = Session()
__all__ = ["session"]
