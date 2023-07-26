from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_409_CONFLICT

from app.database import get_db
from app.models import Vote
from app.oauth2 import get_current_user


router = APIRouter(prefix='/votes', tags=['Votes'])
session = Depends(get_db)


@router.post('/{post_id}/', status_code=status.HTTP_201_CREATED)
def create_vote(post_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    vote = db.query(Vote).filter(Vote.post_id == post_id, Vote.user_id == current_user.id).first()

    if vote:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=f'User {current_user.id} has already voted on post {vote.post_id}'
        )

    new_vote = Vote(user_id=current_user.id, post_id=post_id)
    db.add(new_vote)
    db.commit()


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_vote(post_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    #TODO: add deletion
    pass
