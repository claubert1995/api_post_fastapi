from sqlmodel import Field,Session,SQLModel, create_engine,Relationship
from typing import Optional,List
from config import settings


engine = create_engine(settings.DATABASE_URL)

class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    password: str
    posts: List["Post"] = Relationship(back_populates="author")
    comments: List["Comment"] = Relationship(back_populates="author")

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str 
    content: str 
    id_author: Optional[int] = Field(default=None, foreign_key="author.id")
    # Correction ici : le nom doit être "author" pour correspondre à id_author
    author: Optional["Author"] = Relationship(back_populates="posts")
    comments: List["Comment"] = Relationship(back_populates="posts")

class Comment(SQLModel,table=True):
    id_com: Optional[int] = Field(default=None,primary_key=True)
    content: str | None = None
    id_author: int | None = Field(default=None, foreign_key="author.id")
    id_post: int | None = Field(default=None, foreign_key="post.id")
    author: Optional["Author"] = Relationship(back_populates="comments")
    posts: Optional["Post"] = Relationship(back_populates="comments")

class UpdatePost(SQLModel): 
    title: str | None = None 
    content: str | None = None
    author: str | None = None


def get_session():
    with Session(engine) as session: 
        yield session

def create_db_and_table():
    SQLModel.metadata.create_all(engine)


