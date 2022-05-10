
from models import  engine, Users, Base
from sqlalchemy.orm import sessionmaker
from dependencies import get_password_hash
import fire

class Calculator(object):
  """."""

  def createsuperuser(self, username,password,email="",full_name=""):
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    usersadd=Users()
    usersadd.username=username
    usersadd.hashed_password=get_password_hash(password)
    usersadd.email=email
    usersadd.full_name=full_name
    usersadd.admin=True
    session.add(usersadd)
    session.commit()
    print("SuperUser created ")

if __name__ == '__main__':
  fire.Fire(Calculator)
