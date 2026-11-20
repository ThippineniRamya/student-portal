from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String
from database import Base
class Student(Base):
    __tablename__="student"
    id=Column(Integer,primary_key=True)
    email=Column(String,nullable=False,unique=True)

