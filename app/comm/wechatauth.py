import requests
from loguru import logger

import config as conf


def get_access_token(code):
    a_uri = f'https://api.weixin.qq.com/sns/jscode2session?appid={conf.APPID}&secret={conf.SECRET}&js_code={code}&grant_type=authorization_code'
    resp = requests.get(a_uri)
    data = resp.json()
    logger.debug(data)
    if data.get('openid', None) is None:
        return False

    return data
