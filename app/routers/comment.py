from fastapi import APIRouter, Depends
from app.dependencies import get_token_authorize
from app.dependencies import PageReq
from typing import Union
from doc.comment import Article, ArticleComment, LikeArticle
from app.comm.types import BookCategory
from app.comm.post_data import Book
from mongoengine import Q
import random
from bson import ObjectId
from app.comm.resp import CommonResponse, PageableResponse
import json
