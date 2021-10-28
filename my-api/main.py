from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET /v1/news?from=2021-01-01&to=2021-01-31&category=sport
@app.get("/v1/news", response_model=List[schemas.News])
def read_news_from_date(From: str, to: str, category: str,db:Session =Depends(get_db)):
    return crud.get_news_from_date(db, From=From , to=to, category=category)


@app.post("/news/", response_model=schemas.News)
def create_news(news: schemas.NewsCreate, db: Session = Depends(get_db)):
    db_user = crud.get_news_by_date(db, date=news.date)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, news=news)


@app.get("/news/", response_model=List[schemas.News])
def read_news(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_news(db, skip=skip, limit=limit)
    return users


@app.get("/news/{news_id}", response_model=schemas.News)
def read_user(news_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_news(db, news_id=news_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/news/{news_id}/category/", response_model=schemas.Has_Category)
def create_category_for_news(news_id: int, category: schemas.Has_CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_news_category(db=db, category=category, news_id=news_id)


@app.get("/category/", response_model=List[schemas.Has_Category])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_has_category(db, skip=skip, limit=limit)
    return items


