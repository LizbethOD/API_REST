from fastapi import Depends, FastAPI, HTTPException, status, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import pyrebase

app = FastAPI()

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
    "/user/token/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="GET A TOKEN FOR A USER",
    description="GET A TOKEN FOR A USER",
    tags=["auth"]
    )
def get_token(credentials: HTTPBasicCredentials = Depends(securityBasic)):
    try:
        email = credentials.username
        password = credentials.password
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password(email, password)
        response = {
            "token": user["idToken"]
        }
        return response
    except Exception as error:
        print(f"Error : {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.get(
    "/users/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="GET A USER",
    description="GET A USER",
    tags=["auth"]
    )
async def get_user(credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user["users"][0]['localId']

        db = firebase.database()
        user_data = db.child("users").child(uid).get().val()

        response = {
            'user_data': user_data
        }
        return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)