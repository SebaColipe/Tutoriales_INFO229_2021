from typing import List, Optional

from pydantic import BaseModel


class Has_CategoryBase(BaseModel):
    pass
class Has_CategoryCreate(Has_CategoryBase):
    value: int
    nombre_categoria: str

class Has_Category(Has_CategoryBase):
    

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
    category: str

    class Config:
        orm_mode = True

