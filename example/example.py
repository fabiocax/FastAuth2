from typing import Optional,List

from fastapi import  FastAPI, File, UploadFile, Form,Path,status,HTTPException,Depends,Body,Security
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
import json
from pydantic import BaseModel
from fastapi.security.api_key import APIKeyHeader
import requests


def get_current_active_user(token):
    url = "http://127.0.0.1:8000/api/users/me/"
    payload = ""
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'authorization': "Bearer "+token,
        'cache-control': "no-cache",
        }
    response = requests.request("GET", url, data=payload, headers=headers)

    return [response.status_code, response.text]


JWT_KEY_NAME = "Bearer"

api_key_header_auth = APIKeyHeader(name=JWT_KEY_NAME, auto_error=True)

async def get_api_key(api_key_header: str = Security(api_key_header_auth)):
    ret=get_current_active_user(api_key_header)
    if ret[0] != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return ret[1]


examples = FastAPI()

@examples.get("/teste/")
async def test(retu: dict =Depends(get_api_key)): 
    print(retu)

    
    return JSONResponse({"valid":""})