import re
import uuid
from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.forms import ValidationError
from accounts.models import Profile


class Flower(models.Model):
	name = models.CharField(max_length=100, verbose_name='꽃 이름')
	description = models.TextField(verbose_name='설명')
	price = models.IntegerField(verbose_name='가격 (원)')
	is_best = models.BooleanField(default=False, verbose_name='베스트')
	thumbnail = models.ImageField(
		upload_to='flower/thumbnail',
		verbose_name='썸네일')
	image01 = models.ImageField(
		upload_to='flower/images',
		blank=True,
		verbose_name='이미지01')
	image02 = models.ImageField(
		upload_to='flower/images',
		blank=True,
		verbose_name='이미지02')
	image03 = models.ImageField(
		upload_to='flower/images',
		blank=True,
		verbose_name='이미지03')
	image04 = models.ImageField(
		upload_to='flower/images',
		blank=True,
		verbose_name='이미지04')
	image05 = models.ImageField(
		upload_to='flower/images',
		blank=True,
		verbose_name='이미지05')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	like_user_set = models.ManyToManyField(
		settings.AUTH_USER_MODEL,
		blank=True,
		related_name='like_user_set',
		through='Like',)
	cart_user_set = models.ManyToManyField(
		settings.AUTH_USER_MODEL,
		blank=True,
		related_name='cart_user_set',
		through='Cart',)

	class Meta:
		ordering = ['id']

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:flower_detail', args=[self.id])


class FloImg(models.Model):
	flower = models.ForeignKey(Flower)
	file = models.FileField('FloImg', upload_to='flower/galleries')

	def __str__(self):
		return self.id


class Like(models.Model):
	flower = models.ForeignKey("Flower",)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,)
	created_at = models.DateTimeField(auto_now_add=True,)
	updated_at = models.DateTimeField(auto_now=True,)


class Cart(models.Model):
	flower = models.ForeignKey("Flower",)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,)
	created_at = models.DateTimeField(auto_now_add=True,)
	updated_at = models.DateTimeField(auto_now=True,)


def _createHash():
	unique_id = str(uuid.uuid4())
	return unique_id


class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	order_code = models.CharField(max_length=100, default=_createHash, unique=True)
	receiver_name = models.CharField(max_length=100)
	receiver_phone_number = models.CharField(max_length=11)
	receiver_email = models.EmailField(max_length=100)
	receiver_post_code = models.CharField(max_length=10)
	receiver_address = models.CharField(max_length=50)
	receiver_address_detail = models.CharField(max_length=50)
	pay_type = models.CharField(max_length=50)
	total_price = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True,)
	updated_at = models.DateTimeField(auto_now=True,)

	class Meta:
		ordering = ['-id']

	def __str__(self):
		return self.order_code


class Product(models.Model):
	order = models.ForeignKey(Order)
	flower = models.ForeignKey(Flower)
	count = models.IntegerField()

	def __str__(self):
		return self.flower.name


class Review(models.Model):
	flower = models.ForeignKey(Flower)
	author = models.ForeignKey(settings.AUTH_USER_MODEL)
	subject = models.CharField(max_length=50, verbose_name='제목')
	content = models.TextField(verbose_name='내용')
	image01 = models.ImageField(
		upload_to='review/images',
		blank=True,
		verbose_name='이미지01')
	image02 = models.ImageField(
		upload_to='review/images',
		blank=True,
		verbose_name='이미지02')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-id']

	def __str__(self):
		return self.subject

	def get_edit_url(self):
		return reverse('shop:review_edit', args=[self.flower.pk, self.pk])


class Commentqa(models.Model):
	SUBJECT_CHOICE = (
		('상품문의', '상품문의'),
		('배송문의', '배송문의'),
		('입금문의', '입금문의'),
		('기타문의', '기타문의'),
	)

	flower = models.ForeignKey(Flower)
	author = models.ForeignKey(settings.AUTH_USER_MODEL)
	subject = models.CharField(max_length=50, verbose_name='문의유형',
		choices=SUBJECT_CHOICE)
	content = models.TextField(verbose_name='내용')
	image01 = models.ImageField(
		upload_to='commentqa/images',
		blank=True,
		verbose_name='이미지01')
	image02 = models.ImageField(
		upload_to='commentqa/images',
		blank=True,
		verbose_name='이미지02')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-id']

	def __str__(self):
		return self.subject

	def get_edit_url(self):
		return reverse('shop:commentqa_edit', args=[self.flower.pk, self.pk])


class Rereview(models.Model):
	review = models.OneToOneField(Review)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	content = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.content


class Recommentqa(models.Model):
	commentqa = models.OneToOneField(Commentqa)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	content = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.content