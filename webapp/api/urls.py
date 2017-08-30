from django.conf.urls import url
from . import views

urlpatterns = [
    #/api/users/   get 用户列表  or  post 新用户
    url(r'^users/$', views.user_list, name='users_list'),
    #/api/users/{username}/
    #get  获取用户信息
    #put 修改密码
    #delete 删除用户
    url(r'^users/(?P<pk>[0-9a-zA-Z]+)$', views.user_detail, name='user_detail'),


]
