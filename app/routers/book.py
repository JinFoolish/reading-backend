from fastapi import APIRouter, Depends
from app.dependencies import get_token_authorize
from app.dependencies import PageReq
from typing import Union
from doc.book import BookInfo
from doc.users import UserBook
from app.comm.types import BookCategory
from app.comm.post_data import Book
from mongoengine import Q
import random
from bson import ObjectId
from app.comm.resp import CommonResponse, PageableResponse
import json

router = APIRouter(prefix='/book',tags=['book'],dependencies=[Depends(get_token_authorize)])

@router.get('/list')
async def list_book(user_id:Union[str,None]=None,cate:Union[str,None]=None,query:PageReq=Depends(PageReq)):
    resp = PageableResponse()
    count = BookInfo.objects().count()
    rand_choice = random.randint(0,count-query.size)
    search_q = Q()
    if query.q:
        search_q = search_q & (Q(title__contains=query.q) | Q(author__contains=query.q))
    if cate:
        search_q = search_q & Q(category__eq=cate)
    if user_id:
        search_q = search_q & Q(user_id__eq=user_id)
    data = BookInfo.objects(search_q).order_by('-id').only(*['id','user_id','sentence','cover','title','author']).\
            skip(rand_choice).limit(query.size)
    resp.data = data.to_mongo().to_dict()
    return resp.as_dict()

@router.get('/categories')
async def get_cate():
    resp = CommonResponse()
    data = BookCategory.__dict__['_member_names_']
    resp.data = data
    return resp.as_dict()

@router.post('/create')
async def create(user_id:str, book:Book):
    resp = CommonResponse()
    book = book.dict()
    book['user_id'] = user_id
    book_info = BookInfo()
    book_info.from_json(json.dumps(book),created=True)
    result = book_info.save()
    resp.data = str(result.id)
    return resp.as_dict()

@router.get('/detail')
async def detail(book_id:str):
    resp = CommonResponse()
    data = BookInfo.objects(id=ObjectId(book_id)).first()
    resp.data = data.to_mongo().to_dict()
    return resp.as_dict()

@router.get('/users')
async def users(user_id:str, query:PageReq=Depends(PageReq)):
    resp = PageableResponse()
    data = []
    b_list = UserBook.objects(user_id=user_id).order_by('-id')\
        .skip((query.page - 1) * query.size).limit(query.size)
    for b in b_list:
        data.append(b.book_id)
    resp.data = data
    resp.count = UserBook.objects(user_id=user_id).count()
    return resp.as_dict()

@router.get('/add')
async def like_book(user_id:str, book_id:str):
    resp = CommonResponse()
    exists = UserBook.objects(user_id=user_id,book_id=book_id).first()
    if exists:
        resp.code=99
        resp.msg='already follow'
        return resp.as_dict()
    data_info = UserBook(
        user_id=user_id,
        book_id=book_id
    )
    result = data_info.save()
    resp.data = str(result.id)
    return resp.as_dict()
