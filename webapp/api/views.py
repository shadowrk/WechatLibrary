from django.http import HttpResponse
from ..models import *
import json
import hashlib
from django.core.serializers.json import DjangoJSONEncoder
from utils import encrypt
from itertools import chain
# Create your views here.

#get 获取用户列表
#post  添加新用户
def user_list(request):
	info = 'success created'
	status = 201
	if request.method == 'GET':
		usersSet = User.objects.all().values('id', 'username')
		users = json.dumps(list(usersSet), cls=DjangoJSONEncoder)
		return HttpResponse(users)
	elif request.method == 'POST':
		data = request.body
		req = json.loads(data.decode("UTF-8"))
		username = req['username']
		if not User.objects.filter(username=username).exists():
			user = User.objects.create(username=username, password=encrypt.Encrypt(req['password']))
			try:
				UserDetail.objects.create(user=user, age=req['age'], phonenumber=req['phone'], sex=Sex.objects.get(name=req['sex']))
			except Exception as e:
				info = '参数错误'
				status = 200
				user.delete()
			return HttpResponse(info, status=201)
		else:
			return HttpResponse('用户名已存在')

	else:
		return HttpResponse('error', status=404)

#get 获取username = pk 的用户信息
#put 修改username = pk 的用户密码
#delete  删除用户
def user_detail(request, pk):
	info = 'success modify'
	if request.method == 'GET':
		u = User.objects.filter(username=pk)
		user = list(User.objects.filter(username=pk).values('username'))
		userdetail = list(UserDetail.objects.filter(user=u).values('age', 'phonenumber'))
		usersex = list(Sex.objects.filter(name=UserDetail.objects.get(user=u).sex).values('name'))
		print(type(user), type(userdetail))
		data = json.dumps(userlist, cls=DjangoJSONEncoder)
		return HttpResponse(userlist)
	elif request.method == 'PUT':
		data = request.body
		req = json.loads(data.decode("UTF-8"))
		if User.objects.filter(username=pk).exists():
			user = User.objects.get(username=pk)
			password = user.password
			repassword = req['password']
			if encrypt.Check(password, repassword):
				user.password = encrypt.Encrypt(req['newpassword'])
				user.save()
			else:
				return HttpResponse('mimacuowu', status=500)
			return HttpResponse(info, status=200)
		else:
			return HttpResponse('用户不存在')
	elif request.method == 'DELETE':
		info = 'success delete'
		if User.objects.filter(username=pk).exists():
			user = User.objects.get(id=pk).delete()
			return HttpResponse(info, status=200)
		else:
			return HttpResponse('用户不存在')
