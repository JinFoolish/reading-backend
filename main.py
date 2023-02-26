import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mongoengine import connect, disconnect
from app.dependencies import get_token_authorize
from app.routers import users, admin, follow, book, comment
from app.comm.resp import CommonResponse
from app.comm import wechatauth
from app.comm.jwt import Jwt
from doc.users import User

app = FastAPI()


app.include_router(
    users.router
)
app.include_router(
    follow.router
)
app.include_router(book.router)
app.include_router(comment.router)
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
mongouri = "mongodb+srv://946623679:wohen22002@dududu.hphggp0.mongodb.net/?retryWrites=true&w=majority"

@app.on_event("startup")
async def connect_mongodb():
    connect(host=mongouri)

@app.on_event("shutdown")
async def disconnect_mongodb():
    disconnect()

@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc:Exception):
    return JSONResponse(
        status_code=418,
        content={"message": f"{str(exc)}. There goes a rainbow..."},
    )


@app.get("/login", summary='give me the code get from wechat oauth')
async def login(code:str):
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
    
@app.get('/verify',\
         summary='use this at first each time',\
         description='''it will return you the user id. 
         keep it in the gloabal data, almost every api would use it''')
async def verify(user:dict=Depends(get_token_authorize)):
    resp = CommonResponse()
    resp.data = user['user_id']
    return resp.as_dict()

@app.get('/', response_class=HTMLResponse)
async def index():
    html_file = open("index.html", 'r').read()
    return html_file


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
