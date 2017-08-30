from utils import getAccessToken
import requests
import json

#自定义菜单
def set_Channel():
    appid = 'wx79532da2a5e44511'
    secret = '335b0573b498dfd38db72ccb15cdf0e5'
    token = getAccessToken.get_token()
    url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=' + token
    params = {
        "button":[
            {
                "name":"传送门",
                "type":"view",
                "url":"http://120.25.193.196/webapp/login/"
            }
        ]
    }
    response = requests.post(url, data=json.dumps(params, ensure_ascii=False).encode('UTF-8'))
    return response.json()
