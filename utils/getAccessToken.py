import requests

def get_token():
    appid = 'wx79532da2a5e44511'
    secret = '335b0573b498dfd38db72ccb15cdf0e5'
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appid + '&secret=' + secret
    response = requests.get(url)
    return response.json()['access_token']

def get_infoToken(code):
    appid = 'wx79532da2a5e44511'
    secret = '335b0573b498dfd38db72ccb15cdf0e5'
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid='+ appid +'&secret='+ secret + '&code=' + code +'&grant_type=authorization_code'
    response = requests.get(url)
    return response.json()

def get_info(access_token, openid):
    url = 'https://api.weixin.qq.com/sns/userinfo?access_token=' + access_token + '&openid=' + openid +'&lang=zh_CN'
    response = requests.get(url)
    response.encoding = 'UTF-8'
    return response.json()
