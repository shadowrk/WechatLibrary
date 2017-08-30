from django.conf.urls import url, include
from django.contrib import admin
from WechatLibrary import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^wechat/', include('wechat.urls')),
    url(r'^api/', include('webapp.api.urls')),
    url(r'^webapp/', include('webapp.urls')),
   # url(r'^MP_verify_PuGkBdw2flZxu1Q4.txt', views.text)
]
