import re
from django.forms import ValidationError, TextInput, NumberInput
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from .models import Profile
from django.contrib.auth.models import User
from yamisflower.widgets.post_address_widget import PostAddressWidget


def phone_number_validator(value):
	if not re.match(r'^010[1-9]\d{7}$', value):
		raise ValidationError('정확한 핸드폰 번호를 입력해주세요.')


class SignupForm(UserCreationForm):

	# 전화번호,주소 입력 폼 생성
	username = forms.EmailField(label="이메일")
	password1 = forms.CharField(label=("비밀번호"),
		widget=forms.PasswordInput)
	password2 = forms.CharField(label=("비밀번호 확인"),
		widget=forms.PasswordInput,
		help_text=(""))

	name = forms.CharField(label="이름")
	phone_number = forms.CharField(widget=NumberInput(), label='휴대폰 번호', validators=[phone_number_validator], help_text='\'-\' 를 제외한 숫자만 입력')
	post_code = forms.CharField(widget=PostAddressWidget(), label='우편번호')
	address = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly', 'style':'width:100%;'}), label='도로명 주소')
	address_detail = forms.CharField(widget=forms.TextInput(attrs={'style':'width:100%;'}), label='상세 주소')

	# 그냥 Meta만 쓰면 ModelForm을 불러오려 하기 때문에
	# UserCreationForm의 Meta를 상속받아서 쓴다.
	class Meta:
		model = User
		fields = ("username",)

	def clean_email(self):
		email = self.cleaned_data['username']
		if User.objects.filter(username=username).exists():
			raise ValidationError("이미 등록된 이메일입니다.")
		return email

	def clean_phone_number(self):
		phone_number = self.cleaned_data['phone_number']
		if Profile.objects.filter(phone_number=phone_number).exists():
			raise ValidationError("이미 등록된 번호입니다.")
		return phone_number

	# phone_number와 같은 항목은 UserCreationForm의 기본 필드가 아니므로
	# 따로 함수를 만들어 profile에 저장해줘야한다.
	def save(self):
		# super() 부모 의 save() 함수를 호출한 결과를 user로 받아와 인스턴스 생성
		user = super().save()

		Profile.objects.create(
			user = user, # 위에 super().save()로 받아온 user 인스턴스
			name = self.cleaned_data['name'],
			phone_number = self.cleaned_data['phone_number'],
			post_code = self.cleaned_data['post_code'],
			address = self.cleaned_data['address'],
			address_detail = self.cleaned_data['address_detail'],
		)

		return user


class LoginForm(AuthenticationForm):

	username = forms.EmailField(label="이메일")
	password = forms.CharField(label=("비밀번호"),
		widget=forms.PasswordInput)


class ProfileEditForm(forms.ModelForm):

	name = forms.CharField(label="이름")
	phone_number = forms.CharField(widget=NumberInput(), label='휴대폰 번호', validators=[phone_number_validator], help_text='\'-\' 를 제외한 숫자만 입력')
	post_code = forms.CharField(widget=PostAddressWidget(), label='우편번호')
	address = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly', 'style':'width:100%;'}), label='도로명 주소')
	address_detail = forms.CharField(widget=forms.TextInput(attrs={'style':'width:100%;'}), label='상세 주소')

	class Meta:
		model = Profile
		fields = '__all__'
		widgets = {
			'user': forms.HiddenInput()
		}

	def clean_phone_number(self):
		phone_number = self.cleaned_data['phone_number']

		old_phonenumber = Profile.objects.filter(user_id=self.cleaned_data['user'].id).values('phone_number')
		old_phonenumber = list(old_phonenumber)
		old_phonenumber = old_phonenumber[0]['phone_number']

		if not old_phonenumber == phone_number:
			if Profile.objects.filter(phone_number=phone_number).exists():
				raise ValidationError("이미 등록된 번호입니다.")
		return phone_number


class PasswordEditForm(PasswordChangeForm):
	old_password = forms.CharField(label=("현재 비밀번호"),
		widget=forms.PasswordInput)
	new_password1 = forms.CharField(label=("새로운 비밀번호"),
		widget=forms.PasswordInput)
	new_password2 = forms.CharField(label=("비밀번호 확인"),
		widget=forms.PasswordInput,
		help_text=(""))