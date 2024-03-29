from fastapi import APIRouter, Depends
from app.dependencies import get_token_authorize
from doc.users import User
from bson import ObjectId
from app.comm.resp import CommonResponse, PageableResponse
import json
from typing import List
from doc.users import UserFollow
from doc.comment import LikeArticle
from app.comm.post_data import UserInfo
from app.comm.jwt import Jwt

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_token_authorize)]
)

@router.get("/me")
async def read_user_me(user_id:str):
    user_info = User.objects(id=ObjectId(user_id)).only(*['username','avatar']).first()
    resp = CommonResponse()
    json_data = user_info.to_json()
    json_dict = json.loads(json_data)
    json_dict['user_id'] = user_id
    resp.data = json_dict
    return resp.as_dict()

@router.post("/batch_me")
async def read_users(batch:List[str]):
    resp = PageableResponse()
    data_info = []
    for user_id in batch:
        user_info = User.objects(id=ObjectId(user_id)).only(*['username','avatar']).first()
        if user_info is None:
            continue
        json_data = user_info.to_json()
        json_dict = json.loads(json_data)
        json_dict['user_id'] = user_id
        data_info.append(json_dict)
    resp.list = data_info
    return resp.as_dict()

@router.get('/summary')
async def summ(user_id:str):
    resp = CommonResponse()
    data = {}
    like_count = LikeArticle.objects(user_id=user_id).count()
    follow_to = UserFollow.objects(user_id=user_id).count()
    follow_from = UserFollow.objects(follow_id=user_id).count()
    data['like_count'] = like_count
    data['follow_to'] = follow_to
    data['follow_from'] = follow_from
    resp.data = data
    return resp.as_dict()

@router.post('/save')
async def save(user_info: UserInfo):
    user_info = user_info.dict()
    user = User(**user_info)
    result = user.save()
    resp = CommonResponse()
    resp.data = str(result.id)
    return resp.as_dict()

@router.get('/login')
async def login(openid:str):
    resp = CommonResponse()
    user_info = User.objects(openid=openid).first()
    if user_info:
        token = Jwt.encode({'user_id': str(user_info.id)},
                           3600 * 24 * 365)
        resp.data = {"token": token.decode('utf-8')}
    else:
        resp.data = 0
    
    return resp.as_dict()