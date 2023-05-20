from random import randint,choice

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

names="莫尔索, 塞兹尔, 梅尔索, 雷蒙, 瑟斯特, 玛丽, 阿尔瓦, 安杰鲁, 约瑟芬, 艾米尔, 法官, 路易, 卡利加罗, 约瑟夫, 卡门, 路易丝, 朱利安, 埃米尔, 夏尔, 阿尔贝, 卢西安, 加斯东, 莫里斯, 贝兰松, 阿尔贝特, 约瑟夫, 海伦, 布鲁诺, 奥古斯特, 阿尔文, 莫里斯, 布朗, 萨利, 瓦莱丽, 罗兰, 雅克, 马拉尔梅, 马尔塞尔, 伯尔纳, 莫里斯,达'特阿尼昂, 蒂埃尔, 阿拉米斯, 波尔图斯, 阿多斯, 德·特雷维尔, 费尔南多, 卡米尔, 玛格丽特, 伊莎贝尔, 马塞林, 皮卡尔, 卡蒂纳, 瓦莱尔, 乔凡尼, 雷蒙德, 朱利安, 莫里耶尔, 安德烈, 托尼亚, 基多, 阿尔贝, 拉蒙, 约瑟夫, 卡塞特, 夏洛特, 约翰, 佩皮托, 尤金, 帕西特, 阿尔克塞, 乔治, 伊莎贝尔, 阿格尼丝, 艾伦, 莫雷尔, 普拉西德, 安德尔瓦, 费尔迪南德, 琼, 马拉斯, 拉斐尔, 乔纳森, 艾德蒙, 伊丽莎白, 瓦赫达, 巴鲁夫, 阿比亚塔尔, 卡拉迪乌斯, 比安卡, 瑞乔, 柯斯特, 德维尔, 马提尔德, 莱昂, 阿格拉, 伊希特, 约瑟夫, 蒙泰古, 弗拉瑟特, 阿斯卡尼奥, 卡斯蒂利奥内, 瓦伦丁, 圣玛丽, 奥尔莫, 马蒂诺, 阿尔梅达, 蒙蒂诺, 约瑟夫, 阿萨尔, 埃兹佩兰, 奥斯特, 阿尔比尼, 莱比锡".replace(' ','')
names = names.split(',')

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
    new_user.username = choice(names)
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
