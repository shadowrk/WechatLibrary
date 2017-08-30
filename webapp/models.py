from django.db import models
import django.utils.timezone as timezone
# Create your models here.


#用户表
class User(models.Model):
	phone = models.CharField(max_length=20, primary_key = True)
	password = models.CharField(max_length=100)

	def __str__(self):
		return self.phone

#微信信息
class WechatInfo(models.Model):
	openid = models.CharField(max_length=50)
	nickname = models.CharField(max_length=50)
	province = models.CharField(max_length=20)
	city = models.CharField(max_length=20)

	def __str__(self):
		return self.openid

class Tags(models.Model):
	tag = models.CharField(max_length=100)

	def __str__(self):
		return self.tag

 #书籍
class Book(models.Model):
	 title = models.CharField(max_length=100)
	 image = models.CharField(max_length=100)
	 isbn13 = models.CharField(max_length=14)
	 author = models.CharField(max_length=100)
	 publisher = models.CharField(max_length=100)
	 summary = models.TextField()
	 count = models.IntegerField(default=0)
	 tag = models.ForeignKey(Tags)
	 sum = models.IntegerField(default=0)

	 def __str__(self):
		 return self.title


#用户详细信息表
class UserDetail(models.Model):
	user = models.OneToOneField(User)
	age = models.CharField(max_length=10)
	weinfo = models.OneToOneField(WechatInfo, null=True)
	hobby = models.CharField(max_length=255)
	sex = models.CharField(max_length=10)
	borrowcount = models.IntegerField(default=0)
	def __str__(self):
		return self.phone

class BorrowBooks(models.Model):
	bookname = models.ForeignKey(Book)
	borrowtime = models.DateField(auto_now=True)
	ifback = models.BooleanField(default=False)
	isborrow = models.BooleanField(default=False)
	user = models.ForeignKey(UserDetail)

	def __str__(self):
		return self.bookname

class UserMessage(models.Model):
	user = models.ForeignKey(User)
	mes = models.TextField()
	ifread = models.BooleanField(default=False)

	def __str__(self):
		return self.user


class History(models.Model):
	bookid = models.IntegerField()
	searchtime = models.DateField(auto_now=True)
	user = models.ForeignKey(UserDetail)

	def __str__(self):
		return self.bookid
class BookComment(models.Model):
	book = models.ForeignKey(Book)
	user = models.ForeignKey(User)
	comment = models.TextField()
	time = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return self.bookid

class UsersComment(models.Model):
	user = models.CharField(max_length=100)
	time = models.DateTimeField(default = timezone.now)
	book = models.ForeignKey(BookComment)
	comment = models.TextField()

	def __str__(self):
		return self.user

class Frequency(models.Model):
	user = models.OneToOneField(User)
	fre_time = models.IntegerField(default = 1)

	def __str__(self):
		return self.user

class Reverse(models.Model):
	user = models.ForeignKey(UserDetail)
	book = models.ForeignKey(Book)
	time = models.DateTimeField(auto_now_add=True)
	re_time = models.DateField()

class SuperUser(models.Model):
	user = models.CharField(max_length=100)
	password = models.CharField(max_length=50)

	def __str__(request):
		return self.user
