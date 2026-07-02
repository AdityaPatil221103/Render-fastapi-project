from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models, schemas
from auth import create_token,verify_token

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

#DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#login API
def build_token_response():
    return {
        "access_token": create_token({"user": "admin"}),
        "token_type": "bearer"
    }


@app.post("/login")
def login():
    return build_token_response()


@app.post("/token")
def token():
    return build_token_response()

#Home Route
@app.get("/")
def home():
    return{
        "message":"Blog API started"
    }

#create blog(protected)
@app.post("/blogs",response_model = schemas.BlogResponse)
def create_blog(blog:schemas.BlogCreate, db:Session = Depends(get_db), user = Depends(verify_token)):
    new_blog = models.Blog(
        title = blog.title,
        content = blog.content
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

#read all blog
@app.get("/blogs")
def get_blogs(page: int = 1,
              limit: int = 5,
              search: str = Query(default=""),
              db: Session = Depends(get_db)):

#search logic
    query = db.query(models.Blog)
    if search:
        query = query.filter(models.Blog.title.ilike(f"%{search}%"))

#pagination logic
    total = query.count()
    start = (page - 1)* limit
    blogs = query.offset(start).limit(limit).all()
    
    return{
        "page":page,
        "limit": limit,
        "total": total,
        "data":blogs
    }
              

#read 1 blog
@app.get("/blogs/{id}", response_model=schemas.BlogResponse)
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=404,
            detail= "ID not found"
        )
    return blog

#Update Blog API(Protected)
@app.put("/blogs/{id}", response_model=schemas.BlogResponse)
def update_blog(id: int, blog:schemas.BlogCreate, db: Session = Depends(get_db), user =Depends(verify_token)):
    existing_blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=404,
            detail= "Blog not found"
        )
    
    existing_blog.title = blog.title
    existing_blog.content = blog.content

    db.commit()

    return existing_blog

#delete blog Api(Protected)
@app.delete("/blogs/{id}")
def delete_blog(id: int,db: Session = Depends(get_db), user =Depends(verify_token) ):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog:
        raise HTTPException(
            status_code=404,
            detail= "Blog not found"
        )
    
    blog.delete()
    db.commit()

    return{
        "message":"Blog deleted successfully"
    }
