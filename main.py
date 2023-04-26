from random import randint

import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mongoengine import connect, disconnect
from app.dependencies import get_token_authorize
from app.routers import users, follow, book, comment
from app.comm.resp import CommonResponse
from app.comm import wechatauth
from app.comm.jwt import Jwt
from doc.users import User
import config as con

app = FastAPI()


app.include_router(
    users.router
)
app.include_router(
    follow.router
)
app.include_router(book.router)
app.include_router(comment.router)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def connect_mongodb():
    connect(host=con.MONGOURI)


@app.on_event("shutdown")
async def disconnect_mongodb():
    disconnect()


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=418,
        content={"message": f"{str(exc)}. There goes a rainbow..."},
    )


@app.get("/login", summary='give me the code get from wechat oauth')
async def login(code: str):
    resp = CommonResponse()
    access_data = wechatauth.get_access_token(code)
    if access_data == False:
        resp.msg = 'invalid code'
        resp.code = 100
        return resp.as_dict()
    user_info = User.objects(openid=access_data['openid']).first()
    if user_info:
        token = Jwt.encode({'user_id': str(user_info.id)},
                           3600 * 24 * 365)

        resp.data = {"token": token.decode('utf-8')}

        return resp.as_dict()

    # 微信小程序个人用户信息接口暂不可用，用一些默认值代替一下
    new_user = User()
    new_user.openid = access_data['openid']
    new_user.username = '默认用户'
    new_user.city = '默认地区'
    new_user.country = '中国'
    new_user.avatar = str(randint(1, 148))
    result = new_user.save()
    resp.msg = 'new user'
    token = Jwt.encode({'user_id': str(result.id)},
                       3600 * 24 * 180)
    resp.data = {"token": token.decode('utf-8')}
    return resp.as_dict()


@app.get('/verify',
         summary='use this at first each time',
         description='''it will return you the user id. 
         keep it in the gloabal data, almost every api would use it''')
async def verify(user: dict = Depends(get_token_authorize)):
    resp = CommonResponse()
    resp.data = {'user_id': user['user_id']}
    return resp.as_dict()

@app.get('/', response_class=HTMLResponse)
async def index():
    html_file = open("index.html", 'r').read()
    return html_file


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
