#!/bin/python
from models import  engine, Users, Base
from sqlalchemy.orm import sessionmaker
from dependencies import get_password_hash
import fire
from secrets import token_bytes
from base64 import b64encode
import pyotp 

class Configurator(object):
    """."""
    def createsuperuser(self, username,password,email="",full_name="",otp=False):


        Session = sessionmaker(bind=engine)
        session = Session()
        usersadd=Users()
        usersadd.username=username
        usersadd.hashed_password=get_password_hash(password)
        usersadd.email=email
        usersadd.full_name=full_name
        usersadd.admin=True
        usersadd.otp=otp
        usersadd.otp_secret=pyotp.random_base32()
        session.add(usersadd)
        session.commit()
        print("SuperUser created ")
    def token(self):
        print(b64encode(token_bytes(32)).decode())
if __name__ == '__main__':
    fire.Fire(Configurator)
