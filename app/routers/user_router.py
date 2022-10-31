from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User
from app.schemas import UserRequestSchema, UserResponseSchema
from app.utils import hash_password


router = APIRouter(prefix='/users', tags=['Users'])
session = Depends(get_db)

@router.get('/', response_model=List[UserResponseSchema])
def get_users(db: Session = session):
    users = db.query(User).all()

    return users

@router.get('/{id}/', response_model=UserResponseSchema)
def get_user(id: int, db: Session = session):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User {id} does not exist.')
    
    return user

@router.post('/', response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserRequestSchema, db: Session = session):
    user.password = hash_password(user.password)
    new_user = User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
