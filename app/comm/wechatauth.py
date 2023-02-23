import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_access_token(code):
    access_token_uri = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code={code}&grant_type=authorization_code'
    a_uri = access_token_uri.format(code=code)
    resp = requests.get(a_uri,verify=False)
    data = resp.json()
    if data.get('openid',None) is None:
        return False
    
    return data

def get_user_info(data:dict):
    wechat_info_uri = 'https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}'
    u_uri = wechat_info_uri.format(access_token=data['access_token'],openid=data['openid'])
    resp = requests.get(u_uri,verify=False)
    info = resp.json()
    if info.get('openid',None) is None:
        return False
    
    return info
