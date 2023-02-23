from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.dependencies import get_token_authorize
from app.routers import users, admin
from app.comm.resp import CommonResponse
from app.comm import wechatauth
from app.comm.jwt import Jwt
from doc.users import User
import requests


app = FastAPI()


app.include_router(
    users.router
    )
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_authorize)],
# )
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/login")
async def login(code):
    resp = CommonResponse()
    # code = request.args.get('code',None)
    access_data = wechatauth.get_access_token(code)
    if access_data == False:
        resp.msg = 'invalid code'
        resp.code = 100
        return resp.as_dict()
    user_info = User.objects(openid=access_data['openid'],status=1).first()
    if user_info is not None:
        token = Jwt.encode({'user_id': str(user_info.id)},
                           3600 * 24 * 365)

        resp.data = {"token": token.decode('utf-8')}

        return resp.as_dict()
    
    wechat_user = wechatauth.get_user_info(access_data)
    
    if wechat_user:
        openid = wechat_user['openid']
        nickname = wechat_user['nickname']
        city = wechat_user['city']
        country = wechat_user['country']
        headimgurl = wechat_user['headimgurl']
    else:
        resp.msg = 'invalid openid'
        resp.code = 101
        return resp.as_dict()
    
    new_user = User()
    new_user.openid = openid
    new_user.username = nickname
    new_user.city = city
    new_user.country = country
    new_user.avatar = headimgurl
    result = new_user.save()
    resp.msg = 'new user'
    token = Jwt.encode({'user_id': str(result.id)},
                           3600 * 24 * 180)
    resp.data = {"token": token.decode('utf-8')}
    return resp.as_dict()
    
