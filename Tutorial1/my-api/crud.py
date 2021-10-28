from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode

from . import models, schemas


def get_news(db: Session, news_id: int):
    return db.query(models.News).filter(models.News.id == news_id).first()


def get_news_by_date(db: Session, date: str):
    return db.query(models.News).filter(models.News.date == date).first()


def get_news(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.News).offset(skip).limit(limit).all()


def create_news(db: Session, news: schemas.NewsCreate):
    fake_url = news.url + "notreallyurl"
    fake_title = news.title + "falsoTitulo"
    fake_date = "20-10-2021"
    db_news = models.News(title=fake_title, date = fake_date,url=fake_url, media_outlet = news.media_outlet+"mega")
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news


def get_has_category(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Has_Category).offset(skip).limit(limit).all()


def create_news_category(db: Session, category: schemas.Has_CategoryCreate, news_id: int):
    db_item = models.Has_Category(**category.dict(), new_id=news_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
def get_news_from_date(db: Session, From : str = "2020-01-01", to: str = "2022-01-01", category : str = "sport"):
    return db.query(models.News).filter(models.News.date <= to ).filter(models.News.date >= From ).filter(models.News.category == category ).all()
#.join(models.News, models.News.id ==models.Has_Category.value)
