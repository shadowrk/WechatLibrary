from django.conf.urls import url
from webapp import views

urlpatterns = [

    # url(r'^registercheck/', views.smsCheck),
    url(r'^login/', views.login), #登陆页面
    url(r'^loginCheck/', views.logincheck),
    url(r'^register/$', views.register), #注册
    url(r'^home/$', views.home), #首页
    url(r'^bestseller/$', views.bestseller), #畅销图书榜
    url(r'^smscheck/$', views.smsCheck), #注册发送手机验证码
    # url(r'^addphone/$', views.addPhone),
    url(r'^phonecheck/$', views.phoneCheck), #手机验证
    url(r'^adduser/$', views.addUser),#注册
    url(r'^start/$', views.start),#欢迎页
    url(r'^booklist/', views.search),#搜索框
    url(r'^getbookList/', views.getbookList),#获取搜索的图书列表
    url(r'^getbookDetail/', views.getbookdetail),#获取书籍详情
    url(r'^ajaxgetBook/$', views.ajaxgetbook),
    url(r'^gettypelist/$', views.getTypelist),#获取图书分类列表
    url(r'^typelist/$', views.typeList),#图书分类页面
    url(r'^finder/$', views.Finder),
    url(r'^bookdetail/$', views.bookdetail),#图书详情页面
    # url(r'^test/$', views.test),
    url(r'^getTest/$', views.gettest),
    url(r'^hobby/$', views.hobby),#爱好页面
    url(r'^borrowbooks/$',views.borrows),
    url(r'^borrowbook/$', views.borrowbook),
    url(r'^getBorrowbooks/$', views.getBorrowBooks),
    url(r'^deleteborrowbook/$', views.deleteBorrow),
    url(r'^getcode/$', views.getCode),
    url(r'^usermanage/$', views.Usermanage),
    url(r'^person/$', views.person),
    url(r'^getuser/$', views.getUser),
    url(r'^history/$', views.UserHistory),
    url(r'^gethistory/$', views.getHistory),
    url(r'^settings/$', views.setting),
    url(r'^getmessage/$', views.getMessage),
    url(r'^getrecommend/$', views.getRecommend),
    url(r'^getcomment/$', views.getComment),
    url(r'^setfrequency/$', views.setFrequency),
    url(r'^getfrequency/$', views.getFrequency),
    url(r'^manage-index/$', views.manage),
    url(r'^addbooks/$', views.addBooks),
    url(r'^getbooks/$', views.getBooks),
    url(r'^deletebooks/$', views.deleteBooks),
    url(r'^myqrcode/$', views.myQrcode),
    url(r'^getdetails/$', views.getDetails),
    url(r'^confirm/$', views.Confirm),
    url(r'^commentbook/$', views.commentBook),
    url(r'^usercomment$', views.userComment),
    url(r'^logout/$', views.logout),
    url(r'^reverse/$', views.TReverse),
    url(r'^form/$', views.getform),
    url(r'^ajaxmessage/$', views.ajaxmessage),
    url(r'^getmescount/$', views.getMescount),
    url(r'^getbestseller/$', views.getBestseller),
    url(r'^myreverse/$',views.myReverse),
    url(r'^getmyreverse/$', views.getMyreverse),
    url(r'^borrowslist/$', views.borrowsList),
    url(r'^getborrowslist/$', views.getborrowsList),
    url(r'^models/$', views.model),
    url(r'^scan/$', views.scan),
    url(r'^getdata/$', views.getData)
]
