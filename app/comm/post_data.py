from typing import Union, List
from pydantic import BaseModel, Field

class Book(BaseModel):
    sentence: str = Field(max_length=50)
    cover: str = Field(title='book cover url')
    title: str = Field(max_length=20)
    author: str = Field(max_length=20)
    category: str = Field(title='varieties of book')
    introduce: str = Field(max_length=300)
    rating: int = Field(ge=0,le=10)


class Artic(BaseModel):
    detail: str = Field(max_length=500,title='对于图书的书评感想')
    images: List[str] = Field(default=[],title='图片url列表')
    book_title: str = Field(default='',max_length=20)
    book_id: str = Field(default='')


class ArticComm(BaseModel):
    comment: str = Field(max_length=200)
    article_id: str = Field(title='objectid of article')


class UserInfo(BaseModel):
    openid: str
    username: str
    avatar: str
    city: str = 'unknown'
    country: str = '未知的星球'