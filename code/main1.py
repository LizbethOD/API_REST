from fastapi import Depends, FastAPI, HTTPException, status, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from typing import List
from fastapi import security
from pydantic import BaseModel
from urllib.request import Request
from urllib import response
from lib2to3.pytree import Base
from typing_extensions import Self

import sqlite3
import pyrebase
import hashlib
import os 

app = FastAPI()

DATABASE_URL = os.path.join("sql/clientes.sqlite") 

class Users(BaseModel):
    username : str
    lavel : int

class Respuesta(BaseModel):
    message: str

class Cliente(BaseModel):
    id_cliente: int
    nombre: str
    email: str
    
class UpdateCliente(BaseModel):
    nombre: str
    email : str

class ClienteIN(BaseModel):
    nombre: str
    email: str

origins = [
    "https://8000-lizbethod-apirest-52babcwb66f.ws-us59.gitpod.io/",
    "https://8080-lizbethod-apirest-52babcwb66f.ws-us59.gitpod.io/templates/",
    "*",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/', 
    summary="API-REST")
async def get():
    return "API-REST"

firebaseConfig = {
    'apiKey': "AIzaSyBmKYIgQYdvYQl8PMn7bRefAX7P2xkBCN0",
    'authDomain': "api-firebase-e00d5.firebaseapp.com",
    'databaseURL': "https://api-firebase-e00d5-default-rtdb.firebaseio.com",
    'projectId': "api-firebase-e00d5",
    'storageBucket': "api-firebase-e00d5.appspot.com",
    'messagingSenderId': "326342988677",
    'appId': "1:326342988677:web:bb66f9a6e6d5d637fb6aec"
}

firebase = pyrebase.initialize_app(firebaseConfig)

securityBasic = HTTPBasic()
securityBearer = HTTPBearer()


@app.get(
    "/user/validate/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="SHOW USER TOKEN",
    description="SHOW USER TOKEN",
    tags=["Auth"]
    )
async def get_token(credentials: HTTPBasicCredentials = Depends(securityBasic)):
    try:
        email = credentials.username
        password = credentials.password
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password(email, password)
        response = {
            "token": user["idToken"],
        }
        return response
    except Exception as error:
        print(error)


@app.get(
    "/users/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="GET A USER",
    description="GET A USER",
    tags=["Auth"]
    )
async def get_user(credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId']

        db = firebase.database()
        user_data = db.child("users").child(uid).get().val()
        response = {
            'user_data': user_data}
        return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.get(
    "/clientes/", 
    response_model=List[Cliente],status_code=status.HTTP_202_ACCEPTED,
    summary="SHOWS A LIST OF USERS",
    description="SHOWS A LIST OF USERS",
    tags=["Clientes"]
    )
async def clientes(credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId'] 

        with sqlite3.connect(DATABASE_URL) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM clientes')
            response = cursor.fetchall()
            return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.get(
    "/clientes/{id_cliente}", 
    response_model=List[Cliente],status_code=status.HTTP_202_ACCEPTED, 
    summary="SHOWS A LIST OF CLIENTS ACCORDING TO THEIR ID",
    description="SHOWS A LIST OF CLIENTS ACCORDING TO THEIR ID",
    tags=["Clientes"]
    )
async def clientes(credentials: HTTPAuthorizationCredentials = Depends(securityBearer),id_cliente: int=0):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId'] 

        with sqlite3.connect(DATABASE_URL) as connection:
            connection.row_factory = sqlite3.Row
            cursor=connection.cursor()
            cursor.execute("SELECT * FROM clientes WHERE id_cliente={}".format(int(id_cliente)))
            response=cursor.fetchall()
            return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.post(
    "/clientes/", 
    response_model=Respuesta,
    status_code=status.HTTP_202_ACCEPTED,
    summary="ADD USERS",
    description="ADD USERS",
    tags=["Clientes"]
    )
async def post_cliente( cliente: ClienteIN, credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId'] 

        with sqlite3.connect(DATABASE_URL) as connection:
            connection.row_factory = sqlite3.Row
            cursor=connection.cursor()
            cursor.execute("INSERT INTO clientes(nombre,email) VALUES(?,?)", (cliente.nombre,cliente.email))
            connection.commit()
            response = {"message":"Cliente agregado exitosamente:)"}
            return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.put(
    "/clientes/", 
    response_model=Respuesta,status_code=status.HTTP_202_ACCEPTED,
    summary="UPDATE FROM USERS",
    description="UPDATE FROM USERS",
    tags=["Clientes"]
    )
async def clientes_update(cliente: Cliente, credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
     try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId'] 

        with sqlite3.connect(DATABASE_URL) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("UPDATE clientes SET nombre =?, email= ? WHERE id_cliente =?;",(cliente.nombre, cliente.email, cliente.id_cliente))
            connection.commit()
            response = {"message":"Actualizacion exitosa:)"}
            return response
     except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)  


@app.delete(
    "/clientes/", 
    response_model=Respuesta,status_code=status.HTTP_202_ACCEPTED,
    summary="DELETE USERS",
    description="DELETE USERS",
    tags=["Clientes"]
    )
async def clientes_delete(credentials: HTTPAuthorizationCredentials = Depends(securityBearer), id_cliente: int=0):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId'] 

        with sqlite3.connect('sql/clientes.sqlite') as connection:
            connection.row_factory = sqlite3.Row
            cursor=connection.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente = '{id_cliente}';".format(id_cliente=id_cliente))
            cursor.fetchall()
            response = {"message":"Eliminacion exitosa:("}
            return response
        
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) 
