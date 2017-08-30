from django.conf.urls import url, include
from wechat import views

urlpatterns = [
    #微信开发者验证
    url(r'^wechatCheck/', views.check),
    url(r'^hello/', views.hello),
]
