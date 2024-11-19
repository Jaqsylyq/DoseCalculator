from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Meds(Base):
    __tablename__ = 'medicaments'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)