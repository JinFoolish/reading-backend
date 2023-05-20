from fastapi import APIRouter, Depends
from app.dependencies import PageReq
from doc.users import UserFollow
from app.comm.types import FollowStatus
from app.comm.resp import CommonResponse, PageableResponse
import json


router = APIRouter(
    prefix="/follow",
    tags=["follow"],
)


@router.get('/add')
async def follow_user(follow_id:str, user_id:str):
    resp = CommonResponse()
    exists = UserFollow.objects(user_id=user_id,follow_id=follow_id).first()
    if exists:
        resp.code=99
        resp.msg='already follow'
        return resp.as_dict()
    data_info = UserFollow(
        user_id=user_id,
        follow_id=follow_id
    )
    result = data_info.save()
    resp.data = str(result.id)
    return resp.as_dict()

@router.get('/delete')
async def delete_user(follow_id:str, user_id:str):
    UserFollow.objects(user_id=user_id,follow_id=follow_id).delete()
    return {}

@router.get('/list')
async def follow_list(user_id:str, query:PageReq=Depends(PageReq)):
    resp = PageableResponse()
    data = []
    f_list = UserFollow.objects(user_id=user_id).order_by('-id')\
        .skip((query.page - 1) * query.size).limit(query.size)
    for f in f_list:
        data.append(f.follow_id)
    resp.data = data
    resp.count = UserFollow.objects(user_id=user_id).count()
    return resp.as_dict()

@router.get('/judge')
async def judge_follow(follow_id:str, user_id:str):
    resp = CommonResponse()
    exist_1 = UserFollow.objects(user_id=user_id,follow_id=follow_id).first()
    exist_2 = UserFollow.objects(user_id=follow_id,follow_id=user_id).first()
    if exist_1:
        resp.data = FollowStatus.FOLLOW_TO.value
    if exist_1 and exist_2:
        resp.data = FollowStatus.FOLLOW_BOTH.value
    return resp.as_dict()