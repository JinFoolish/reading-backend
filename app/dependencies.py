from fastapi import Header, HTTPException
from app.comm.jwt import Jwt
from typing import Union

async def get_token_authorize(x_token: str = Header()):
    if len(x_token) < 50:
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    user_info = Jwt.decode(x_token.encode('utf-8'))
    if user_info is None:
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return {'user_id':user_info['user_id']}

class PageReq:
    def __init__(self, page:int=1, size:int=5, q:Union[str,None]=None) -> dict:
        self.page = page
        self.size = size
        self.q = q