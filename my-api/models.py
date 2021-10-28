from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base #Se importa el objeto Base desde el archivo database.py

class News(Base): 

    __tablename__ = "news"

    id = Column(Integer,unique=True, primary_key=True, index=True)
    title = Column(String(150), unique=True, index=True)
    date = Column(String(50))
    url = Column(String(350), unique=True)
    media_outlet = Column(String(50), index=True)
    category = Column(String(50), primary_key=True)
    
    #categorias = relationship("Has_Category", back_populates="noticias")

class Has_Category(Base):

    __tablename__ = "has_category"
    nombre_categoria = Column(String(50),primary_key=True, index=True)
    value = Column(Integer, ForeignKey("news.id"))

#    noticias = relationship("News", back_populates="categorias")
