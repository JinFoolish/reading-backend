from fastapi import APIRouter, Depends
from app.dependencies import get_token_authorize
from app.dependencies import PageReq
from typing import Union, List
from app.comm.types import LikeStatus
from doc.comment import Article, ArticleComment, LikeArticle, LikeComment
from app.comm.post_data import Artic, ArticComm
from mongoengine import Q
import random
from bson import ObjectId
from app.comm.resp import CommonResponse, PageableResponse
import json
from datetime import datetime

router = APIRouter(
    prefix='/comment',
    tags=['comment'],
    dependencies=[Depends(get_token_authorize)]
)

@router.get('/list/artical',
           summary='you can get random articles',
           description='''
                if give a 'q', db will query related book title which contains 'q',
                if give a book_id, db wikk query related book id which equal it.
           ''')
async def list_artical(book_id:Union[str,None]=None, query:PageReq=Depends(PageReq)):
    resp = PageableResponse()
    search_q = Q()
    data = []
    if query.q:
        search_q = search_q & Q(book_title__contains=query.q)
    if book_id:
        search_q = search_q & Q(book_id=book_id)
    count = Article.objects(search_q).count()
    if count==0:
        resp.data = 'no record'
        resp.code = 99
        return resp.as_dict()
    rand_choice = random.randint(0,count-query.size-1)
    data_info = Article.objects(search_q).skip(rand_choice).limit(query.size)
    for i in data_info:
        data.append(i.to_mongo().to_dict())
    resp.data = data
    resp.count = count
    return resp.as_dict()

@router.get('/list/artical/user')
async def user_artic(user_id:str, query:PageReq=Depends(PageReq)):
    resp = PageableResponse()
    data = []
    data_info = Article.objects(user_id=user_id).order_by('-id')\
            .skip((query.page - 1) * query.size).limit(query.size)
    for i in data_info:
        data.append(i.to_mongo().to_dict())
    resp.data = data
    resp.count = Article.objects(user_id=user_id).count()
    return resp.as_dict()

@router.get('/batch_list/article')
async def batch_article(batch:List[str]):
    resp = PageableResponse()
    data_info = []
    for article_id in batch:
        article_info = Article.objects(id=ObjectId(article_id)).first()
        if article_info is None:
            continue
        data = article_info.to_mongo().to_dict()
        data_info.append(data)
    resp.data = data_info
    return resp.as_dict()

@router.post('/create/article')
async def create_article(user_id:str, article:Artic):
    resp = CommonResponse()
    article = article.dict()
    article['user_id'] = user_id
    article_info = Article.from_json(json.dumps(article),created=True)
    article_info.create_time = datetime.now()
    result = article_info.save()
    resp.data = str(result.id)
    return resp.as_dict()

@router.get('/like/article')
async def like_article(user_id:str,article_id:str):
    resp = CommonResponse()
    exists = LikeArticle.objects(user_id=user_id,article_id=article_id).first()
    if exists:
        resp.code=99
        resp.msg='already like'
        return resp.as_dict()
    data_info = LikeArticle(
        user_id=user_id,
        article_id=article_id
    )
    result = data_info.save()
    resp.data = str(result.id)
    return resp.as_dict()

@router.get('/judge/article')
async def judge_article(user_id:str, batch:List[str]):
    resp = PageableResponse()
    data_info = []
    for article_id in batch:
        d = {}
        exists = LikeArticle.objects(user_id=user_id,article_id=article_id).first()
        count = LikeArticle.objects(article_id=article_id).count()
        d['count'] = count
        if exists:
            d[article_id] = LikeStatus.LIKE.value
        else:
            d[article_id] = LikeStatus.NOLIKE.value
        data_info.append(d)
    resp.data = data_info
    return resp.as_dict()

@router.get('/users/article', summary='get articles liked by a user')
async def users_article(user_id:str, query:PageReq=Depends(PageReq)):
    resp = PageableResponse()
    data = []
    a_list = LikeArticle.objects(user_id=user_id).order_by('-id')\
        .skip((query.page - 1) * query.size).limit(query.size)
    for a in a_list:
        data.append(a.article_id)
    resp.data = data
    resp.count = LikeArticle.objects(user_id=user_id).count()
    return resp.as_dict()

@router.post('/create/comment')
async def create_comment(user_id:str, comment:ArticComm):
    resp = CommonResponse()
    comment = comment.dict()
    comment['user_id'] = user_id
    comment_info = ArticleComment.from_json(json.dumps(comment),created=True)
    comment_info.create_time = datetime.now()
    result = comment_info.save()
    resp.data = str(result.id)
    return resp.as_dict()

@router.get('/list/comment')
async def list_comment(article_id:str, query:PageReq=Depends(PageReq)):
    resp = PageableResponse()
    data = []
    data_info = ArticleComment.objects(article_id=article_id).order_by('-id')\
            .skip((query.page - 1) * query.size).limit(query.size)
    resp.count = ArticleComment.objects(article_id=article_id).count()
    for i in data_info:
        data.append(i.to_mongo().to_dict())
    resp.data = data
    return resp.as_dict()

@router.get('/judge/comment')
async def judge_comment(user_id:str, batch:List[str]):
    resp = PageableResponse()
    data_info = []
    for comment_id in batch:
        d = {}
        exists = LikeComment.objects(user_id=user_id,comment_id=comment_id).first()
        count = LikeComment.objects(comment_id=comment_id).count()
        d['count'] = count
        if exists:
            d[comment_id] = LikeStatus.LIKE.value
        else:
            d[comment_id] = LikeStatus.NOLIKE.value
        data_info.append(d)
    resp.data = data_info
    return resp.as_dict()

@router.get('/like/comment')
async def like_comment(user_id:str, comment_id:str):
    resp = CommonResponse()
    exists = LikeComment.objects(user_id=user_id,comment_id=comment_id).first()
    if exists:
        resp.code=99
        resp.msg='already like'
        return resp.as_dict()
    data_info = LikeArticle(
        user_id=user_id,
        comment_id=comment_id
    )
    result = data_info.save()
    resp.data = str(result.id)
    return resp.as_dict()