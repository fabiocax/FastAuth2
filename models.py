from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Text, BOOLEAN
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from os import environ
import datetime
from dependencies import *

try:
    SQLALCHEMY_DATABASE_URL=environ["API_DATABASE_URL"]     
except:
    SQLALCHEMY_DATABASE_URL = "sqlite:///db/fast.db"
#SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


#engine = create_engine(
#    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
#)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String, unique=False, index=True)
    email = Column(String, unique=False, index=True)
    hashed_password = Column(String)
    token_timeout = Column(Integer, default=10)
    admin = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)
    def as_dict(self):
       return {c.key: getattr(self, c.key) for c in self.__table__.columns}


#Criando usuario de teste




