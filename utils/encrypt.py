from django.contrib.auth.hashers import make_password, check_password

#密码加密
def Encrypt(password):
    enc_password = make_password(password)
    return enc_password

#密码验证
#password  数据库中的密码
#repassword post的密码
def Check(password, repasssword):
    return check_password(repasssword, password)
