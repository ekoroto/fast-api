from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Post
from app.oauth2 import get_current_user
from app.schemas import PostResponseSchema, PostRequestSchema

router = APIRouter(prefix='/posts', tags=['Posts'])
session = Depends(get_db)

@router.get('/', response_model=List[PostResponseSchema])
def get_posts(limit: int = 10, offset: int = 0, db: Session = session, current_user = Depends(get_current_user)):
    posts = db.query(Post).filter(Post.user_id == current_user.id).limit(limit).offset(offset).all()

    return posts

@router.get('/{id}/', response_model=PostResponseSchema)
def get_post(id: int, db: Session = session, current_user = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} was not found.')

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Not authorized to perform requested action.')

    return post

@router.post('/', response_model=PostResponseSchema, status_code=status.HTTP_201_CREATED)
def create_posts(post: PostRequestSchema, db: Session = session, current_user = Depends(get_current_user)):
    new_post = Post(user_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.put('/{id}/', response_model=PostResponseSchema)
def update_post(id: int, new_post: PostRequestSchema, db: Session = session,
        current_user: int = Depends(get_current_user)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} was not found.')

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Not authorized to perform requested action.')

    post_query.update(new_post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)

    return post

@router.delete('/{id}/')
def delete_post(id: int, db: Session = session, current_user = Depends(get_current_user)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} does not exist.')

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Not authorized to perform requested action.')

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
