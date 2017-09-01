from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	# 하나의 Profile 레코드가 하나의 User 레코드와 OneToOne 관계를 맺음
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	name = models.CharField(max_length=20,
		help_text='실명 입력을 권장합니다.')
	phone_number = models.CharField(max_length=11,
		help_text='\'-\' 를 제외한 숫자만 입력')
	post_code = models.CharField(max_length=10)
	address = models.CharField(max_length=50)
	address_detail = models.CharField(max_length=50)

	def __str__(self):
		return self.name