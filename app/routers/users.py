from fastapi import APIRouter, Depends
from app.dependencies import get_token_authorize
from doc.users import User
from bson import ObjectId
from app.comm.resp import CommonResponse, PageableResponse
import json
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"]
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
async def read_user(batch:List[str], dependencies=[Depends(get_token_authorize)]):
    resp = PageableResponse()
    data_info = []
    for id in batch.id_list:
        user_info = User.objects(id=ObjectId(id)).only(*['username','avatar']).first()
        if user_info is None:
            continue
        json_data = user_info.to_json()
        json_dict = json.loads(json_data)
        json_dict['user_id'] = id
        data_info.append(json_dict)
    resp.data = data_info
    return resp.as_dict()

