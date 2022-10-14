
from fastapi import APIRouter, Depends, HTTPException
from dependencies import *
from fastapi import FastAPI,status,HTTPException,Depends,Response
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models import  engine, Users,Parameters
from sqlalchemy.orm import sessionmaker, exc
import random
import hashlib
from dependencies import *
import qrcode 
from io import BytesIO
import pyotp
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v2/authentication/token")

def uuid():
	return hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()



def get_db():
    Session = sessionmaker(bind=engine)
    return Session()

	
def user_details(username):
	
	try:
		ret=get_db.query(Users).filter(Users.username ==username,Users.disabled==False).one()
	except:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="User disabled",
			headers={"WWW-Authenticate": "Bearer"},
		)
	return ret

oauth = APIRouter(
    prefix="/api/v2",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@oauth.post("/authentication/token", response_model=Token)
async def login_for_access_token(session: Session = Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends(),token_timeout: int = Form(None)):

	try:
		userdb=session.query(Users).filter(Users.username == form_data.username,Users.disabled==False).one()
		if userdb.token_revoque==True:
			userdb.token_revoque=False
			session.commit()

		users_db={form_data.username:userdb.as_dict()}
		user = authenticate_user(users_db, form_data.username, form_data.password,form_data.client_secret)


	except exc.NoResultFound:
		if ldap_test().ldap(form_data.username,form_data.password)==True:
			user={'username':form_data.username}
	try:
		if not user:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Incorrect username or password",
				headers={"WWW-Authenticate": "Bearer"},
			)
	except:
		raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Not authorized",
				headers={"WWW-Authenticate": "Bearer"},
			)

	user_parms=session.query(Parameters).filter(Parameters.parent_id== userdb.id)
	dict_parameters={}
	if token_timeout == None:
		ttout= userdb.token_timeout
	else:
		ttout=token_timeout

	for line in user_parms:
		dict_parameters[line.key_name]=line.value
	access_token_expires = timedelta(minutes=ttout)
	

	access_token = create_access_token(
		data={"sub": user.username,"parms": dict_parameters}, expires_delta=access_token_expires
	)
	return {"access_token": access_token, "token_type": "bearer"}

@oauth.get("/authentication/users/")
async def get_user_info(session: Session = Depends(get_db),current_user: User = Depends(get_current_active_user),expires: float = Depends(get_expires_token),parms: dict = Depends(get_parms)):
	
	userdb=session.query(Users).with_entities(Users.disabled, Users.token_revoque).filter(Users.username == current_user.username).one()
	if (userdb.disabled == True) or (userdb.token_revoque==True):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authorized",
			headers={"WWW-Authenticate": "Bearer"},
		)
	
	ret={"username":current_user.username,
		 "token_expire":expires,
		 "parms": parms
		 }
	return ret


@oauth.get("/adm/users/{username}", response_model=User)
async def get_username_info(username: str,current_user: User = Depends(get_current_active_user)):
	userd =user_details(current_user.username)
	if userd.admin == True:
		uuser=user_details(username)
		ret={"user_id":uuser.id,
			"username":uuser.username,
			"email":uuser.email,
			"full_name":uuser.full_name,
			}
	else:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authorized",
			headers={"WWW-Authenticate": "Bearer"},
		)
	return ret

@oauth.post("/adm/users/", response_model=User)
async def add_users(session: Session = Depends(get_db),current_user: User = Depends(get_current_active_user),username: str = Form(...),password: str = Form(None),email: str = Form(...),fullname: str = Form(...),token_timeout: int=15,otp_active: bool=False):
	userd =user_details(current_user.username)
	if userd.admin == True:

		usersadd=Users()
		usersadd.username=username
		if password ==None:
			usersadd.hashed_password="ldap"
		else:
			usersadd.hashed_password=get_password_hash(password)
		usersadd.email=email
		usersadd.full_name=fullname
		usersadd.admin=False
		usersadd.token_timeout=token_timeout
		usersadd.otp=otp_active
		usersadd.otp_secret=pyotp.random_base32()
		session.add(usersadd)
		try:
			session.commit()
		except:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="UNIQUE constraint failed",
				headers={"WWW-Authenticate": "Bearer"},
			)
	else:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authorized",
			headers={"WWW-Authenticate": "Bearer"},
		)
	ret={"username":username,"email":email,"full_name":fullname}
	return ret

@oauth.delete("/adm/users/", response_model=User)
async def delete_user_info(session: Session = Depends(get_db),current_user: User = Depends(get_current_active_user),username: str = Form(...)):
	userd =user_details(current_user.username)
	if userd.admin == True:

		session.query(Users).filter(Users.username == username).delete()
		session.commit()
	else:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authorized",
			headers={"WWW-Authenticate": "Bearer"},
		)
	ret={"username":username}

	return ret

@oauth.put("/adm/users/", response_model=User)
async def disabled_user_info(session: Session = Depends(get_db),current_user: User = Depends(get_current_active_user),username: str = Form(...),disabled: bool = Form(...)):
	userd =user_details(current_user.username)
	if userd.admin == True:

		session.query(Users).filter(Users.username == username).update({Users.disabled:disabled})
		session.commit()
	else:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authorized",
			headers={"WWW-Authenticate": "Bearer"},
		)
	ret={"username":username}

	return ret

@oauth.post("/adm/users/parameters/add/{username_id}")
async def add_parameters_users(username_id: str,session: Session = Depends(get_db),current_user: User = Depends(get_current_active_user),key: str = Form(...),value: str = Form(...)):
	userd =user_details(current_user.username)
	if userd.admin == True:

		parms=Parameters()
		parms.parent_id=username_id
		parms.key_name=key
		parms.value=value
		session.add(parms)
		try:
			session.commit()
		except:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="UNIQUE constraint failed",
				headers={"WWW-Authenticate": "Bearer"},
			)
	else:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authorized",
			headers={"WWW-Authenticate": "Bearer"},
		)
	ret={"username":"true"}
	return ret

@oauth.get("/adm/users/parameters/list/{username_id}")
async def get_username_parms_list(username_id: str,session: Session = Depends(get_db),current_user: User = Depends(get_current_active_user)):
	
	userd =user_details(current_user.username)
	if userd.admin == True:
		user_parms=session.query(Parameters).filter(Parameters.parent_id== username_id)
		dict_parameters=[]
		for line in user_parms:
			dict_parameters.append(line.__dict__)
	else:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authorized",
			headers={"WWW-Authenticate": "Bearer"},
		)
	return dict_parameters

@oauth.delete("/adm/users/parameters/list/{key_id}")
async def delete_username_parms(key_id: str,session: Session = Depends(get_db),current_user: User = Depends(get_current_active_user)):
	
	userd =user_details(current_user.username)
	if userd.admin == True:
	
		user_parms=session.query(Parameters).filter(Parameters.id== key_id).delete()
		session.commit()

	else:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authorized",
			headers={"WWW-Authenticate": "Bearer"},
		)
	ret={"key_id":key_id}

	return ret



@oauth.get("/adm/users/otp/qrcode/{username}", response_model=User)
async def get_otp_qrcode(username: str,current_user: User = Depends(get_current_active_user),box_size: int=5):
	userd =user_details(current_user.username)
	if userd.admin == True:
		uuser=user_details(username)

		uri = pyotp.totp.TOTP(uuser.otp_secret).provisioning_uri(name=uuser.email, issuer_name='fastauth2')

		qr = qrcode.QRCode(box_size=box_size)
		qr.add_data(uri)
		qr.make(fit=True)
		image = qr.make_image(fill_color='black', back_color='white')

		filtered_image = BytesIO()
		image.save(filtered_image, "JPEG")
		filtered_image.seek(0)

	else:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authorized",
			headers={"WWW-Authenticate": "Bearer"},
		)
	return StreamingResponse(filtered_image, media_type="image/png")

@oauth.get("/adm/users/otp/id/{username}", response_model=User)
async def get_otp_userid(username: str,token: int,current_user: User = Depends(get_current_active_user)):
	userd =user_details(current_user.username)
	token_valid=False
	if userd.admin == True:
		uuser=user_details(username)
		totp = pyotp.TOTP(uuser.otp_secret)
		if token ==int(totp.now()):
			token_valid=True
		else:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Token Invalid",
				headers={"WWW-Authenticate": "Bearer"},
			)			

	else:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authorized",
			headers={"WWW-Authenticate": "Bearer"},
		)
	ret={"username":uuser.username,"otp_token":token_valid,'email':""}

	return ret