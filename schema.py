from db_connection import Base
from sqlalchemy import Column, String, Integer

class tab(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    actual_url = Column(String, unique=True, index=True)
    short_url = Column(String, unique=True, index=True)