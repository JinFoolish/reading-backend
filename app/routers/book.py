from fastapi import APIRouter, Depends
from app.dependencies import get_token_authorize
from app.dependencies import PageReq
from typing import Union, List
from datetime import datetime
from doc.book import BookInfo
from doc.users import UserBook
from app.comm.types import BookCategoryEnum, LikeStatus
from app.comm.post_data import Book
from mongoengine import Q
import random
from bson import ObjectId
from app.comm.resp import CommonResponse, PageableResponse
import json

router = APIRouter(prefix='/book',tags=['book'],dependencies=[Depends(get_token_authorize)])

@router.get('/list', 
            summary='get a book info list',
            description='''
                if give a q, db will query the title or author which contains q,
                if give cate, db will query category which equals cate,
            ''')
async def list_book(cate:Union[str,None]=None,query:PageReq=Depends(PageReq)):
    resp = PageableResponse()
    search_q = Q()
    data = []
    if query.q:
        search_q = search_q & (Q(title__contains=query.q) | Q(author__contains=query.q))
    if cate:
        search_q = search_q & Q(category=cate)
    count = BookInfo.objects(search_q).count()
    if count==0:
        resp.data = 'no record'
        resp.code = 99
        return resp.as_dict()
    rand_choice = random.randint(0,count-query.size-1)
    data_info = BookInfo.objects(search_q)\
            .exclude('introduce')\
            .skip(rand_choice).limit(query.size)
    for i in data_info:
        d = i.to_mongo().to_dict()
        d["_id"] = str(d['_id'])
        data.append(d)
    resp.list = data
    resp.count = count
    return resp.as_dict()

@router.get('/list/user', summary="get books created by a user")
async def list_user_book(user_id:str, query:PageReq=Depends(PageReq)):
    resp = PageableResponse()
    data = []
    data_info = BookInfo.objects(user_id=user_id).order_by('-id')\
            .exclude('introduce')\
            .skip((query.page - 1) * query.size).limit(query.size)
    for i in data_info:
        d = i.to_mongo().to_dict()
        d['_id'] = str(d['_id'])
        data.append(d)
    resp.list = data
    resp.count = BookInfo.objects(user_id=user_id).count()
    return resp.as_dict()


@router.get('/batch_list',
            summary="use to get book info in the user's LIKE",
            description='''
                give a list of book id
            ''')
async def batch_list(batch:List[str]):
    resp = PageableResponse()
    data_info = []
    for book_id in batch:
        book_info = Book.objects(id=ObjectId(book_id)).exclude('introduce').first()
        if book_info is None:
            continue
        data = book_info.to_mongo().to_dict()
        data_info.append(data)
    resp.data = data_info
    return resp.as_dict()

@router.get('/categories', summary='return type of categories')
async def get_cate():
    resp = CommonResponse()
    data = BookCategoryEnum.__dict__['_member_names_']
    resp.data = data
    return resp.as_dict()

@router.post('/create')
async def create(user_id:str, book:Book):
    resp = CommonResponse()
    book = book.dict()
    book['user_id'] = user_id
    book_info = BookInfo.from_json(json.dumps(book),created=True)
    book_info.create_time = datetime.now()
    result = book_info.save()
    resp.data = str(result.id)
    return resp.as_dict()

@router.get('/detail')
async def detail(book_id:str):
    resp = CommonResponse()
    data = BookInfo.objects(id=ObjectId(book_id)).first()
    resp.data = data.to_mongo().to_dict()
    return resp.as_dict()

@router.get('/judge')
async def judge(user_id:str, batch:List[str]):
    resp = PageableResponse()
    data_info = []
    for book_id in batch:
        d = {}
        exists = UserBook.objects(user_id=user_id,book_id=book_id).first()
        count = UserBook.objects(book_id=book_id).count()
        d['count'] = count
        if exists:
            d[book_id] = LikeStatus.LIKE.value
        else:
            d[book_id] = LikeStatus.NOLIKE.value
        data_info.append(d)
    resp.data = data_info
    return resp.as_dict()

@router.get('/users', summary='get books liked by a user')
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
        resp.msg='already like'
        return resp.as_dict()
    data_info = UserBook(
        user_id=user_id,
        book_id=book_id
    )
    result = data_info.save()
    resp.data = str(result.id)
    return resp.as_dict()
