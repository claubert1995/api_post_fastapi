from datetime import timedelta
from fastapi import APIRouter,Form,File,UploadFile,Depends,HTTPException
from .base import create_db_and_table, get_session, Post, UpdatePost, Author
from sqlmodel import Session,select
from typing import List,Annotated
from pydantic import BaseModel
from config import settings
from .auth import get_password_hash,Token,verify_password,create_access_token,decode_token,TokenData
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.on_event("startup")
def startup():
    create_db_and_table()

#route for sign up author
@router.post("/add_author",response_model=Author)
async def add_author(author: Author, session: Session = Depends(get_session)):
    author.password = get_password_hash(author.password)
    session.add(author)
    session.commit()
    session.refresh(author)
    return author

# Route for obtain token JWT
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):

    author = session.exec(select(Author).where(Author.name == form_data.username)).first()

    if not author or not verify_password(form_data.password, author.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        data={"sub": author.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

#route for list of post
@router.get("/")
def get_posts(session: Session=Depends(get_session)):
    posts = session.exec(select(Post)).all()
    return [
        {
            **post.dict(),
            "author": post.author.dict(exclude={"password"}) if post.author else None
        }
        for post in posts
    ]


#route for get post by id
@router.get("/post/{id_post}")
async def get_on_post(id_post: int,session: Session=Depends(get_session)):
    # Requête pour récupérer un seul post avec son auteur
    post = session.exec(select(Post).where(Post.id == id_post)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    author = session.exec(select(Author).where(Author.id == post.id_author)).first()
    
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "id_author": post.id_author,
        "author": {
            "name": author.name
        }
    }

#route for add post
@router.post("/add",response_model = Post)
async def add_one_post(post: Post,session: Session = Depends(get_session),token: str = Depends(oauth2_scheme)):
    token_data = decode_token(token)
    author = session.exec(select(Author).where(Author.name == token_data.username)).first()
   
    if author is None:
        raise HTTPException(status_code=404, detail="User not found")

    post.id_author = author.id 
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

#route for delete one post
@router.delete("/delete/{id_post}")
async def delete_one_post(id_post: int,session: Session = Depends(get_session),token: str = Depends(oauth2_scheme)):
    token_data = decode_token(token)
    author = session.exec(select(Author).where(Author.name == token_data.username)).first()
    if author is None:
        raise HTTPException(status_code=404, detail="User not found")

    stm = select(Post).where(Post.id == id_post)
    result = session.exec(stm)
    post = result.one()
    session.delete(post)
    session.commit()
    return {"Sucess"}

#route for update post
@router.patch("/update/{id_user}",response_model=Post)
async def update_one_post(id_user: int ,post_data: UpdatePost, session: Session = Depends(get_session),token:str = Depends(oauth2_scheme)):
    token = decode_token(token)

    stm = session.get(Post,id_user)
    if not token.username:
        raise HTTPException(status_code=404,detail="Post or User not found")

    data = post_data.model_dump(exclude_unset=True)
    stm.sqlmodel_update(data)

    session.add(stm)
    session.commit()
    session.refresh(stm)
    return stm

    