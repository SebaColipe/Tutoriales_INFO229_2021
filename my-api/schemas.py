from typing import List, Optional

from pydantic import BaseModel


class Has_CategoryBase(BaseModel):
    news_id: int

class Has_CategoryCreate(Has_CategoryBase):
    pass

class Has_Category(Has_CategoryBase):
    value: str
    

    class Config:
        orm_mode = True

class NewsBase(BaseModel):
    title: str

class NewsCreate(NewsBase):
    url: str

class News(NewsBase):
    id: int
    date: str
    media_outlet: str
    categorias: List[Has_Category] = []

    class Config:
        orm_mode = True

