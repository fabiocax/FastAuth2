from fastapi import Header, HTTPException


from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from fastapi import FastAPI, File, UploadFile, Form,Path,status,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from os import environ
from sqlalchemy.orm import sessionmaker
from secrets import token_bytes
from base64 import b64encode
import pyotp
from ldap_auth import ldap_test

app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v2/authentication/token")
try:
    SECRET_KEY=environ["SECRET_KEY"]
except:

    SECRET_KEY = b64encode(token_bytes(32)).decode() ## openssl rand -hex 32

ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    user_id: Optional[int]=None
    username: str
    #email: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    expire: Optional[float] = None
    otp_token: Optional[bool] = None


class UserInDB(User):
    hashed_password: str
    otp_secret: str
    otp: bool
    
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str,client_secret:str):
    user = get_user(fake_db, username)
    if not user.hashed_password=='ldap':
        if not user:
            return False
        
        if not verify_password(password, user.hashed_password):
            return False

    else:
        ldap_auth=ldap_test()
        if ldap_auth.ldap(username,password) == False:
            return False

    if user.otp ==True:
        totp = pyotp.TOTP(user.otp_secret)
        if not client_secret == totp.now():
            return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data

async def get_expires_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        curr_dt = datetime.now()
        timestamp = int(round(curr_dt.timestamp()))
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expires: timedelta = payload.get("exp")
        expire=((expires-timestamp))

        #expire = datetime.utcnow() - expires
    except JWTError:
        raise credentials_exception
    return expire

async def get_parms(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        parms=payload.get("parms")
    except JWTError:
        raise credentials_exception
    return parms

async def get_current_active_user(current_user: User = Depends(get_current_user)):
 
    return current_user

