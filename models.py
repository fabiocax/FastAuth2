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
    SQLALCHEMY_DATABASE_URL = "sqlite:///sql_tmp.db"

#print("INFO:     Select database: "+SQLALCHEMY_DATABASE_URL)


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
    token_revoque = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)
    parms = Column(Text, default='{}')
    otp = Column(Boolean, default=True)
    otp_secret= Column(String)
    def as_dict(self):
       return {c.key: getattr(self, c.key) for c in self.__table__.columns}

class Parameters(Base):
    __tablename__ = "parameters"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("users.id"))
    key_name = Column(String, unique=False, index=True)
    value = Column(String, unique=False)
    
#Criando usuario de teste


Base.metadata.bind = engine
Base.metadata.create_all(engine)

