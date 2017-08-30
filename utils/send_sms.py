import requests

#发送短信验证码
#vertifycode 验证码
#mobile 手机号
def sendSms(vertifycode, mobile):
    account = 'C90920887'
    password = '173dd895796f286f7c0fb8271d130377'
    url = 'http://106.ihuyi.com/webservice/sms.php?method=Submit'
    text = '您的验证码是：' + vertifycode + '。请不要把验证码泄露给其他人。'
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = {'account': account, 'password': password, 'mobile': mobile, 'content': text, 'format': 'json'}
    r = requests.post(url, data=params, headers=headers)
    return r.json()
