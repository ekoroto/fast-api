from jose import jwt, JWTError
from datetime import datetime, timedelta

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import TokenDataSchema

SECRET_KEY = '234780tcy7n038cty230ty203tym20349tyxmc104tyn2ct'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode['exp'] = expire

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')

        if not user_id:
            raise credentials_exception

        token_data = TokenDataSchema(id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(OAUTH2_SCHEME), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})

    token_data = verify_access_token(token, credentials_exception)

    user = db.query(User).filter(User.id == token_data.id).first()

    return user
