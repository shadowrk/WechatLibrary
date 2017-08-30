import requests
def getTicket(token):
    url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=" + token + "&type=jsapi"
    response = requests.get(url)
    response.encoding = 'UTF-8'
    # if response.json['errmsg'] == 'ok':
    #     return response.json['ticket']
    # else:
    #     return None
    return response.json()['ticket']
