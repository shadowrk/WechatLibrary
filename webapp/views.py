from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from utils import send_sms, getAccessToken
from django.core.serializers.json import DjangoJSONEncoder
from webapp.models import *
from utils import encrypt, getAccessToken, getticket, sign
from django.utils.encoding import smart_str
import urllib
import qrcode
from PIL import Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
import time
import datetime, calendar
# Create your views here.

#短信验证
@csrf_exempt
def smsCheck(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('UTF-8'))
        vertifycode = data['code']
        mobile = data['phone']
        rejson = send_sms.sendSms(vertifycode, mobile)
        code = rejson['code']
        if code == 2:
            return HttpResponse('提交成功')
        elif code == 0:
            return HttpResponse('提交失败')
        elif code == 4030:
            return HttpResponse('手机号码已被列入黑名单')
        else:
            return HttpResponse('发送短信失败')
    else:
        return HttpResponse(status=404)

#手机号验证页�?@csrf_exempt
def phoneCheck(request):
    return render(request, 'phonecheck.html')

#添加注册手机号到session
# @csrf_exempt
# def addPhone(request):
#     if request.method == 'POST':
#         return HttpResponse('success')
#     return HttpResponse('failed')

#注册信息页面
@csrf_exempt
def register(request):
    return render(request, 'register.html')


#注册成功并返回appid, code
@csrf_exempt
def addUser(request):
    appid = 'wx79532da2a5e44511'
    redirect_uri = 'http://trycreat.cn/webapp/home/'
    dict = {
    "redirect_uri":redirect_uri
    }
    data = urllib.parse.urlencode(dict)
    if request.method == 'POST':
        try:
            phone = request.POST.get('phone')
            password = encrypt.Encrypt(request.POST.get('password'))
            user = User.objects.create(phone=phone, password=password)
            age = request.POST.get('age')
            hobby = request.POST.get('hobby')
            sex = request.POST.get('sex')
            userdetail = UserDetail.objects.create(user=user, age=age, hobby=hobby, sex=sex)
            result = {
            "code":"success",
            "appid":appid,
            "data":data
            }
            return HttpResponse(json.dumps(result), content_type="application/json")
        except Exception as e:
            user = User.objects.get(phone=phone)
            if user.exists() and not UserDetail.objects.get(user=user).exists():
                user.delete()
            return HttpResponse(json.dumps({"code":"failed"}), content_type='application/json')
    return HttpResponse(json.dumps({"code":"failed"}), content_type='application/json')
@csrf_exempt
def scan(request):
    return render(request, 'manager.html')
#登录页面
@csrf_exempt
def login(request):
    if request.session.get('id', None) == None:
        return render(request, 'login.html')
    else:
        return HttpResponseRedirect('../home')

@csrf_exempt
def logincheck(request):
    if request.method == 'POST':
        phone = request.POST.get('username')
        password = request.POST.get('password')
        try:
            if User.objects.filter(phone=phone).exists():
                user = User.objects.get(phone=phone)
                if encrypt.Check(user.password, password):
                    request.session['id'] = phone
                    return HttpResponse('success')
                else:
                    return HttpResponse('failed', status=404)
            elif SuperUser.objects.filter(user=phone).exists():
                user = SuperUser.objects.get(user=phone)
                if password == user.password:
                    return HttpResponse('admin')
                else:
                    return HttpResponse('failed', status=404)

        except:
            return HttpResponse('failed', status=404)
    else:
        return HttpResponse('failed', status=404)

@csrf_exempt
def hobby(request):
    return render(request, 'hobby.html')
#首页
#首次注册自动绑定微信�?@csrf_exempt
def home(request):
    if request.GET.get('code') != None:
        phone = request.GET.get('state')
        user = User.objects.get(phone=phone)
        userdetail = UserDetail.objects.get(user=user)
        code = request.GET.get('code')
        response = getAccessToken.get_infoToken(code)
        access_token = response.get('access_token')
        openid = response.get('openid')
        data = getAccessToken.get_info(access_token, openid)
        weinfo = WechatInfo.objects.create(openid=data.get('openid'), nickname=data.get('nickname'), province=data.get('province'), city=data.get('city'))
        userdetail.weinfo = weinfo
        userdetail.save()
        request.session['id'] = phone
    return render(request, 'index.html')

#欢迎页面
@csrf_exempt
def start(request):
    return render(request, 'start.html')
@csrf_exempt
def bestseller(request):
    tag = request.GET.get('type')
    return render(request, 'bestseller.html', {'type':json.dumps(tag)})
@csrf_exempt
def search(request):
    if request.method == 'POST':
        searchValue = request.POST.get('searchValue')
        return render(request, 'booklist.html', {'searchValue':json.dumps(searchValue)})
    return HttpResponse(status=400)

@csrf_exempt
def ajaxgetbook(request):
    name = request.GET.get('name')
    try:
        book = Book.objects.filter(title__icontains=name).values('id', 'title')[:5]
        return HttpResponse(json.dumps(list(book)), content_type='application/json')
    except:
        return HttpResponse(status=400)
@csrf_exempt
def getbookList(request):
    if request.method == 'GET':
        start = int(request.GET.get('start'))
        name = request.GET.get('name')
        booklist = []
        if len(Book.objects.filter(title__icontains=name)) != 0:
            book = Book.objects.filter(title__icontains=name).values('id', 'title', 'image')[start:start+10]
            for i in book:
                booklist.append(i)
            return HttpResponse(json.dumps(booklist), content_type='application/json')
        elif len(Book.objects.filter(author__icontains=name)) != 0:
            book = Book.objects.filter(author__icontains=name).values('id', 'title', 'image')[start:start+10]
            for i in book:
                booklist.append(i)
            return HttpResponse(json.dumps(booklist), content_type='application/json')
        elif len(Book.objects.filter(isbn13=name)) != 0:
            book = Book.objects.filter(isbn13=name).values('id', 'title', 'image')[start:start+10]
            for i in book:
                booklist.append(i)
            return HttpResponse(json.dumps(booklist), content_type='application/json')
    return HttpResponse(status=400)


@csrf_exempt
def getbookdetail(request):
    if request.method == 'GET':
        id = request.GET['id']
        phone = request.session['id']
        try:
            user = User.objects.get(phone=phone)
            userinfo = UserDetail.objects.get(user=user)
            book = Book.objects.filter(id=id).values('id', 'image', 'title', 'isbn13', 'publisher', 'summary', 'author', 'count')
            tag = Tags.objects.get(tag=Book.objects.get(id=id).tag)
            flag = History.objects.filter(user=userinfo, bookid=id).exists()
            if flag:
                his = History.objects.get(user=userinfo, bookid=id)
                his.save()
            else:
                History.objects.create(user=userinfo, bookid=id)
            booklist = []
            for i in book:
                booklist.append(i)

            books = tag.book_set.all()
            l = []
            for i in books:
                images={}
                if len(l) >= 5:
                    break
                a = random.randint(1,20)
                if a % 5 == 0:
                    images['image'] = i.image
                    images['id'] = i.id
                    l.append(images)
                else:
                    continue

            booklist.append(l)
            return HttpResponse(json.dumps(booklist), content_type="application/json")
        except Exception as e:
            print(e)
            return HttpResponse(status=400)
    return HttpResponse(status=400)

@csrf_exempt
def bookdetail(request):
    id = request.GET.get('id')
    return render(request, 'bookdetail.html', {'bookid': id})

@csrf_exempt
def borrows(request):
    return render(request, 'borrow_books.html')
@csrf_exempt
def getBorrowBooks(request):
    if request.method == 'GET':
        phone = request.session['id']
        try:
            user = User.objects.get(phone=phone)
            userdetail = UserDetail.objects.get(user=user)
            borrows = userdetail.borrowbooks_set.filter(isborrow=False, ifback=False)
            books = []
            for book in borrows:
                books.append({
                'id': book.bookname.id,
                'title': book.bookname.title,
                'author': book.bookname.author,
                'image': book.bookname.image
                })
            return HttpResponse(json.dumps(books), content_type='application/json')
        except Exception as e:
            print(e)
            return HttpResponse(status=400)
    return HttpResponse(status=500)

@csrf_exempt
def borrowbook(request):
    phone = request.session['id']
    bookid = request.GET.get('bookid')
    try:
        user = User.objects.get(phone=phone)
        userdetail = UserDetail.objects.get(user=user)
        book = Book.objects.get(id=bookid)
        if userdetail.borrowcount < 2 and book.count > 0:
            try:
                if len(BorrowBooks.objects.filter(user=userdetail, bookname=book, isborrow=False)) > 0:
                    return HttpResponse('此书以存在借书栏')
                else:
                    borrowbook = BorrowBooks.objects.create(user=userdetail, bookname=book)
                    return HttpResponse('加入借书栏成功')
            except Exception as e:
                print(e)
                return HttpResponse(status=400)
        else:
            return HttpResponse('借阅失败')
    except Exception as e:
        print(e)
        return HttpResponse(status=400)
@csrf_exempt
def deleteBorrow(request):
    phone = request.session['id']
    bookid = request.GET.get('id')
    try:
        user = User.objects.get(phone=phone)
        userdetail = UserDetail.objects.get(user=user)
        book = Book.objects.get(id=bookid)
        borrow = BorrowBooks.objects.get(user=userdetail, bookname=book, isborrow=False)
        borrow.delete()
        return HttpResponse('success')
    except Exception as e:
        print(e)
        return HttpResponse('error')

@csrf_exempt
def Finder(request):
    return render(request, 'find.html')

@csrf_exempt
def getCode(request):
    phone = request.session['id']
    stats = request.GET.get('stats')
    books = request.GET.getlist('bookIds[]')
    userdetail = UserDetail.objects.get(user=User.objects.get(phone=phone))
    if userdetail.borrowcount + len(books) > 2:
        return HttpResponse('借阅失败')
    else:
        if stats == '0':
            data = '-'.join(books)
            url = 'http://trycreat.cn/webapp/myqrcode/?stats=0&bookids=' + data + '&id=' + phone
        else:
            data = '-'.join(books)
            url = 'http://trycreat.cn/webapp/myqrcode/?stats=1&bookids=' + data + '&id=' + phone
        qr=qrcode.QRCode(version=4,
                     error_correction=qrcode.constants.ERROR_CORRECT_L,
                     box_size=8,
                     border=8,
                     )
        qr.add_data(url)
        qr.make(fit=True)
        img=qr.make_image()
        l = [stats, phone, str(len(books))]
        t = '-'.join(l)
        img.save('/home/webapp/WechatLibrary/static/qrcode/'+ t +'.png')
        return HttpResponse(t)

@csrf_exempt
def person(request):
    return render(request, 'person.html')

@csrf_exempt
def getUser(request):
    id = request.session['id']
    try:
        user = User.objects.get(phone=id)
        userdetail = UserDetail.objects.filter(user=user).values('user', 'age', 'sex')
        userinfo = []
        for i in userdetail:
            userinfo.append(i)
        return HttpResponse(json.dumps(userinfo), content_type='application/json')
    except Exception as e:
        print(e)
        return HttpResponse(status=400)

@csrf_exempt
def UserHistory(request):
    return render(request, 'history.html')

@csrf_exempt
def getHistory(request):
    id = request.session['id']
    try:
        user = User.objects.get(phone=id)
        userdetail = UserDetail.objects.get(user=user)
        history = userdetail.history_set.all()
        books = []
        for i in history:
            book = Book.objects.get(id=i.bookid)
            bookinfo = {}
            bookinfo['searchtime'] = str(i.searchtime)
            bookinfo['id'] = book.id
            bookinfo['title'] = book.title
            bookinfo['image'] = book.image
            bookinfo['author'] = book.author
            bookinfo['publisher'] = book.publisher
            books.append(bookinfo)
        books.reverse()
        return HttpResponse(json.dumps(books), content_type='application/json')
    except Exception as e:
        print(e)
        return HttpResponse(status=400)


@csrf_exempt
def Usermanage(request):
    id = request.session['id']
    return render(request, 'User_manage.html', {'username':id})
@csrf_exempt
def setting(request):
    return render(request, 'setting.html')
# @csrf_exempt
# def test(request):
#     d = ['back', 80]
#     t = ['borrow', 20]
#     l = [d, t]
#     return render(request, 'test.html', {'data' : l})
@csrf_exempt
def gettest(request):
    token = getAccessToken.get_token()
    ticket = getticket.getTicket(token)
    signature = sign.Sign(ticket, request.GET.get('url'))
    data = signature.sign()
    print(data)
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def getMessage(request):
    id = request.session['id']
    # id = '17806240279'
    user = User.objects.get(phone=id)
    message = user.usermessage_set.all().values('mes')

    return HttpResponse(json.dumps(list(message)), content_type='application/json')

@csrf_exempt
def getRecommend(request):
    recommend_list = Book.objects.all().values('id', 'title', 'image')[:4]
    return HttpResponse(json.dumps(list(recommend_list)), content_type='application/json')

@csrf_exempt
def getComment(request):
    id = request.GET.get('id')
    book = Book.objects.get(id=id)
    b_comment = BookComment.objects.filter(book=book)
    data = []
    for b in b_comment:
        u_comment = b.userscomment_set.all()
        users = []
        for u in u_comment:
            user = User.objects.get(phone = u.user)
            d = {}
            d['phone'] = user.phone
            d['time'] = u.time.strftime("%Y-%m-%d %H:%I:%S")
            d['comment'] = u.comment
            users.append(d)
        dic = {}
        dic['phone'] = b.user.phone
        dic['time'] = b.time.strftime("%Y-%m-%d %H:%I:%S")
        dic['comment'] = b.comment
        dic['users'] = users
        data.append(dic)
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def setFrequency(request):
    id = request.session.get('id')
    fre_time = request.POST.get('time')
    print(fre_time)
    user = User.objects.get(phone = id)
    fre = Frequency.objects.get(user=user)
    fre.fre_time = fre_time
    fre.save()
    return HttpResponse(status=200)

@csrf_exempt
def getFrequency(request):
    id = request.session.get('id')
    user = User.objects.get(phone = id)
    fre = Frequency.objects.get(user=user)
    time = fre.fre_time
    return HttpResponse(time)


#管理�?@csrf_exempt
def manage(request):
    return render(request, 'manage.html')

@csrf_exempt
def addBooks(request):
    if request.method == 'POST':
        name = request.POST.get('bookName')
        author = request.POST.get('bookAuthor')
        isbn = request.POST.get('bookISBN')
        publisher = request.POST.get('bookPublish')
        count = request.POST.get('bookStock')
        tag = request.POST.get('bookType')
        t = Tags.objects.get(tag=tag)
        if not Book.objects.filter(title=name, isbn13=isbn, publisher=publisher, author=author, tag=t).exists():
            Book.objects.create(title=name, isbn13=isbn, publisher=publisher, author=author, count=count, tag=t)
            return HttpResponse('添加成功')
        else:
            return HttpResponse('书籍已存在')
    return HttpResponse('添加失败', status=400)

@csrf_exempt
def getBooks(request):
    page = int(request.GET.get('page'))
    books = Book.objects.filter(id__range=[(page-1)*50, page*50]).values('title', 'author', 'publisher', 'count', 'isbn13', 'tag__tag')
    l = []
    d = dict()
    d['esg'] = 'ok'
    d['nextpage'] = page+1
    d['result'] = list(books)
    l.append(d)
    return HttpResponse(json.dumps(l), content_type='application/json')

@csrf_exempt
def deleteBooks(request):
    try:
        title = request.POST.get('bookName')
        author = request.POST.get('bookAuthor')
        publisher = request.POST.get('bookPublish')
        isbn13 = request.POST.get('bookISBN')
        count = request.POST.get('bookStock')
        print(author)
        book = Book.objects.get(title=title, author=author, publisher=publisher, isbn13=isbn13)
        book.delete()
    except Exception as e:
        print(e)
    return HttpResponse('删除成功')

@csrf_exempt
def myQrcode(request):
    stats = request.GET.get('stats')
    b_ids = request.GET.get('bookids')
    #print(b_ids)
    phone = request.GET.get('id')
    if stats == '0':
        return render(request, 'manage-borrow.html', {'bookIds': json.dumps(b_ids), 'phone': phone})
    else:
        return render(request, 'manage- examine.html', {'bookIds': json.dumps(b_ids), 'phone': phone})

@csrf_exempt
def getDetails(request):
    stats = request.GET.get('stats')
    bookIds = request.GET.get('bookIds')
    b_ids = str(bookIds).split('-')
    books = []
    for book in b_ids:
        b = Book.objects.get(id=int(book))
        d = dict()
        d['title'] = b.title
        d['author'] = b.author
        d['image'] = b.image
        d['id'] = b.id
        books.append(d)
    return HttpResponse(json.dumps(books), content_type='application/json')

@csrf_exempt
def Confirm(request):
    stats = str(request.GET.get('stats'))
    bookIds = request.GET.get('id')
    phone = request.GET.get('phone')
    b_ids = str(bookIds).split('+')
    user = User.objects.get(phone=phone)
    userdetail = UserDetail.objects.get(user=user)
    #print(stats)
    if stats == '0':
        for id in b_ids:
            try:
                userdetail.borrowcount += 1
                userdetail.save()
                book = Book.objects.get(id=id)
                book.count = book.count - 1
                book.save()
                borrow = BorrowBooks.objects.get(user=userdetail, bookname=book, isborrow=False)
                borrow.isborrow = True
                borrow.save()
            except Exception as e:
                print(e)
        return HttpResponse('借阅成功')
    else:
        for id in b_ids:
            try:
                userdetail.borrowcount -= 1
                userdetail.save()
                book = Book.objects.get(id=id)
                book.count = book.count + 1
                book.save()
                borrow = BorrowBooks.objects.get(user=userdetail, bookname=book)
                borrow.ifback = True
                borrow.save()
            except Exception as e:
                print(e)
        return HttpResponse('归还成功')
@csrf_exempt
def typeList(request):
    tag = request.GET.get('tag')
    print(tag)
    return render(request, 'booktypelist.html', {'tag':json.dumps(tag)})
@csrf_exempt
def getTypelist(request):
    start = int(request.GET.get('start'))
    tag = request.GET.get('type')
    g_tag = Tags.objects.get(tag=tag)
    books = g_tag.book_set.all().values('id', 'image', 'title', 'count', 'author')[start:start+10]
    return HttpResponse(json.dumps(list(books)), content_type='application/json')
@csrf_exempt
def getform(request):
    return render(request, 'form.html')
@csrf_exempt
def getData(request):
    now = time.localtime()
    year = now[0]
    mouth = now[1]
    days = calendar.monthrange(year, mouth)[1]
    # tags = ['科技', '生活', '小说', '文学', '旅游', '美食', '少儿', '励志', '历史', '教辅']
    if request.GET.get('stats') == '1':
        tags = Tags.objects.all()
        data = []
        for tag in tags:
            l = {}
            count = 0
            books = tag.book_set.all()
            for book in books:
                b_book = book.borrowbooks_set.filter(borrowtime__range=(datetime.date(year, mouth, 1), datetime.date(year, mouth, days)))
                count += len(b_book)
            l['name'] = tag.tag
            l['count'] = count
            data.append(l)
            print(tag.tag)
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        now = time.localtime()
        year = now[0]
        mouth = now[1]
        f_mouth = (mouth-2+12)%12 if (mouth-2+12)%12 != 0 else 12
        s_mouth = (mouth-1+12)%12 if (mouth-1+12)%12 != 0 else 12
        days = calendar.monthrange(year, f_mouth)[1]
        days1 = calendar.monthrange(year, s_mouth)[1]
        days2 = calendar.monthrange(year, mouth)[1]
        borrows1 = BorrowBooks.objects.filter(borrowtime__range=(datetime.date(year, f_mouth, 1), datetime.date(year, f_mouth, days)))
        borrows2 = BorrowBooks.objects.filter(borrowtime__range=(datetime.date(year, s_mouth, 1), datetime.date(year, s_mouth, days1)))
        borrows3 = BorrowBooks.objects.filter(borrowtime__range=(datetime.date(year, mouth, 1), datetime.date(year, mouth, days2)))
        data = [[str(f_mouth)+'月份', len(borrows1)], [str(s_mouth)+'月份', len(borrows2)], [str(mouth)+'月份', len(borrows3)]]
        return HttpResponse(json.dumps(data), content_type='json')

@csrf_exempt
def commentBook(request):
    bookId = request.POST.get('bookId')
    value = request.POST.get('value')
    id = request.session['id']
    user = User.objects.get(phone=id)
    book = Book.objects.get(id=bookId)
    bookcomment = BookComment.objects.create(book=book, user=user, comment=value)
    l = []
    data = dict()
    data['id'] = id
    data['comment'] = value
    data['time'] = str(bookcomment.time)
    l.append(data)
    return HttpResponse(json.dumps(l), content_type='application/json')

@csrf_exempt
def userComment(request):
    id = request.session['id']
    phone = request.POST.get('phone')
    bookId = request.POST.get('bookId')
    value = request.POST.get('value')
    book = Book.objects.get(id=bookId)
    user = User.objects.get(phone=phone)
    comment = BookComment.objects.get(user=user, book=book)
    usercomment = UserComment.objects.create(user=id, book=comment, comment=value)
    data = {
    'value': value
    }
    msg = "用户"+id+"评论了您: "+value
    usermessage = UserMessage.objects.create(user=user, mes=mes)
    return HttpResponse(data)
@csrf_exempt
def logout(request):
    del request.session['id']
    return HttpResponse(status=200)

@csrf_exempt
def myReverse(request):
    id = request.session['id']
    bookid = request.GET.get('bookId')
    date = request.GET.get('date')
    user = User.objects.get(phone=id)
    userdetail = UserDetail.objects.get(user=user)
    book = Book.objects.get(id=bookid)
    my_reverse = Reverse.objects.create(user=userdetail, book=book, re_time=date)
    return HttpResponse('success')

@csrf_exempt
def ajaxmessage(request):

    id = request.session['id']
    user = User.objects.get(phone=id)
    userdetail = UserDetail.objects.get(user=user)
    borrowbooks = userdetail.borrowbooks_set.filter(isborrow=True, ifback=False)
    for book in borrowbooks:
        date1 = book.borrowtime
        date2 = datetime.date.today()
        if (date2-date1).days <= 7:
            mes = '您借阅的'+book.bookname.title+'还有'+str((date2-date1).days)+'天到期，请尽快归还'
            if user.usermessage_set.filter(mes__contains='您借阅的'+book.bookname.title):
                u_mes = user.usermessage_set.filter(mes__contains=book.bookname.title)[0]
                u_mes.mes = mes
                u_mes.save()
            else:
                UserMessage.objects.create(user=user, mes=mes)
    return HttpResponse('success', status=200)

@csrf_exempt
def getMescount(request):
    id = request.session['id']
    user = User.objects.get(phone=id)
    messages = user.usermessage_set.filter(ifread=False)
    return HttpResponse(str(len(messages)))

@csrf_exempt
def getBestseller(request):
    type = request.GET.get('type')
    def dict2list(dic:dict):
        ''' 将字典转化为列表 '''
        keys = dic.keys()
        vals = dic.values()
        lst = [(key, val) for key, val in zip(keys, vals)]
        return lst
    if type == 'day' or type == 'week':
        date = datetime.date.today()
        books = BorrowBooks.objects.filter(borrowtime=date)
        data = dict()
        for book in books:
            key = book.bookname.title
            if key in data:
                data[key] = data[key]+1
            else:
                data[key] = 1
        sorted_data = sorted(dict2list(data), key=lambda x:x[0], reverse=True)
        l = []
        for d in sorted_data:
            dic = {}
            b = Book.objects.get(title=d[0])
            dic['title'] = d[0]
            dic['image'] = b.image
            dic['author'] = b.author
            dic['publisher'] = b.publisher
            dic['id'] = b.id
            l.append(dic)
        return HttpResponse(json.dumps(l), content_type='application/json')
    elif type == 'month':
            now = time.localtime()
            year = now[0]
            mouth = now[1]
            days = calendar.monthrange(year, mouth)[1]
            borrows = BorrowBooks.objects.filter(borrowtime__range=(datetime.date(year, mouth, 1), datetime.date(year, mouth, days)))
            data = dict()
            for book in borrows:
                key = book.bookname.title
                if key in data:
                    data[key] = data[key]+1
                else:
                    data[key] = 1
            sorted_data = sorted(dict2list(data), key=lambda x:x[0], reverse=True)
            l = []
            for d in sorted_data:
                dic = {}
                b = Book.objects.get(title=d[0])
                dic['title'] = d[0]
                dic['image'] = b.image
                dic['author'] = b.author
                dic['publisher'] = b.publisher
                dic['id'] = b.id
                l.append(dic)
            return HttpResponse(json.dumps(l), content_type='application/json')
@csrf_exempt
def TReverse(request):
    return render(request, 'myreverse.html')

@csrf_exempt
def getMyreverse(request):
    id = request.session['id']
    user = User.objects.get(phone=id)
    userdetail = UserDetail.objects.get(user=user)
    books = userdetail.reverse_set.all().values('book__id', 'book__image', 'book__title', 'book__author', 'book__tag', 're_time')
    for i in books:
        i['re_time'] = str(i['re_time'])
    return HttpResponse(json.dumps(list(books)), content_type='application/json')
@csrf_exempt
def borrowsList(request):
    return render(request, 'myborrows.html')
@csrf_exempt
def getborrowsList(request):
    id = request.session['id']
    user = User.objects.get(phone=id)
    u_detail = UserDetail.objects.get(user=user)
    books = u_detail.borrowbooks_set.filter(isborrow=True, ifback=False).values('borrowtime', 'bookname__id', 'bookname__title', 'bookname__author', 'bookname__image')
    for i in books:
        i['borrowtime'] = str(i['borrowtime'])
    return HttpResponse(json.dumps(list(books)), content_type='application/json')

@csrf_exempt
def model(request):
    return render(request, 'model.html')
