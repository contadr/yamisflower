import json
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from django.contrib.auth.views import login as auth_login
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, QueryDict, JsonResponse
from .forms import LoginForm, SignupForm, AuthenticationForm, ProfileEditForm, PasswordEditForm
from .models import Profile
from shop.models import Cart, Flower, Order, Product


def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save()
			messages.success(request, '{} 님의 회원가입을 환영합니다!'.format(user.profile))
			return redirect(settings.LOGIN_URL)
	else:
		# form = UserCreationForm()
		form = SignupForm()
	return render(request, 'accounts/signup_form.html', {
		'form' : form,
	})

# 로그인이 되어있을 시에만 profile을 보여준다.
# 로그인이 안되어있으면 자동으로 login_required를 통해 login 페이지로 이동
@login_required
def profile(request):

	# OAuth를 통한 로그인일 경우 처음에 Profile 필드가 없다.
	# 이때문에 확인하여 생성해준다.
	if not Profile.objects.filter(user_id=request.user.id):
		Profile.objects.create(
			user = request.user,
			name = '',
			phone_number = '',
			post_code = '',
			address = '',
			address_detail = '',
		)

	return render(request, 'accounts/profile.html')


def login(request):
    providers = []
    for provider in get_providers():  # settings/INSTALLED_APPS 내에서 활성화된 목록
        # social_app속성은 provider에는 없는 속성입니다.
        try:
            # 실제 Provider 별 Client id/secret 이 등록이 되어있는가?
            provider.social_app = SocialApp.objects.get(provider=provider.id, sites=settings.SITE_ID)
        except SocialApp.DoesNotExist:
            provider.social_app = None
        providers.append(provider)

    return auth_login(request,
        authentication_form=LoginForm,
        template_name='accounts/login_form.html',
        extra_context={'providers': providers})


@login_required
def profile_edit(request):

	if not Profile.objects.filter(user_id=request.user.id):
		Profile.objects.create(
			user = request.user,
			name = '',
			phone_number = '',
			post_code = '',
			address = '',
			address_detail = '',
		)

	profile = get_object_or_404(Profile, user_id=request.user.id)

	if request.method == 'POST':
		form = ProfileEditForm(request.POST, instance=profile)
		if form.is_valid():
			user = form.save()
			messages.success(request, '기본 정보를 변경하였습니다.')
			return redirect('/accounts/profile/')
	else:
		form = ProfileEditForm(instance=profile)

	return render(request, 'accounts/profile_edit_form.html', {
		'form': form,
	})


@login_required
def password_edit(request):

	if request.method == 'POST':
		form = PasswordEditForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, '비밀번호 변경 완료')
			return redirect('/accounts/profile/')
		else:
			messages.error(request, '비밀번호를 다시 입력해주세요.')
	else:
		form = PasswordEditForm(request.user)
	return render(request, 'accounts/password_edit_form.html', {
		'form': form
	})


@login_required
def like_list(request):
	return render(request, 'accounts/like_list.html', {
		'flower_list': request.user.like_user_set.all(),
	})


@login_required
def cart_list(request):
	carts = Cart.objects.filter(user_id=request.user.id).prefetch_related('flower')

	return render(request, 'accounts/cart_list.html', {
		'cart_list': carts,
	})


@login_required
def order_list(request):

	order_list = Order.objects.filter(user_id=request.user.id).values()

	return render(request, 'accounts/order_list.html', {
		'order_list': order_list,
	})


@login_required
def product_list(request):
	if request.method == 'POST':

		product_list = Product.objects.filter(order_id=request.POST.get('order_id')).prefetch_related('flower')

		flower_list = []
		for product in product_list:
			flower_list.append({
				'count': product.count,
				'flower_id': product.flower.id,
				'flower_name': product.flower.name,
				'flower_price': product.flower.price*product.count,
				'flower_thumbnail': product.flower.thumbnail.url
			})

		return HttpResponse(json.dumps(flower_list), content_type='application/json')

