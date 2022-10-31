from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Post
from app.schemas import PostResponseSchema, PostRequestSchema

router = APIRouter(prefix='/posts', tags=['Posts'])
session = Depends(get_db)

@router.get('/', response_model=List[PostResponseSchema])
def get_posts(db: Session = session):
    posts = db.query(Post).all()

    return posts

@router.get('/{id}/', response_model=PostResponseSchema)
def get_post(id: int, db: Session = session):
    post = db.query(Post).filter(Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} was not found.')
    
    return post

@router.post('/', response_model=PostResponseSchema, status_code=status.HTTP_201_CREATED)
def create_posts(post: PostRequestSchema, db: Session =session):
    new_post = Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.put('/{id}/', response_model=PostResponseSchema)
def update_post(id: int, new_post: PostRequestSchema, db: Session = session):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} was not found.')
    
    post_query.update(new_post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)

    return post

@router.delete('/{id}/')
def delete_post(id: int, db: Session = session):
    post = db.query(Post).filter(Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} does not exist.')
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
