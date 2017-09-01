from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
# from .forms import LoginForm


urlpatterns = [
	url(r'^signup/$', views.signup, name='signup'),

	url(r'^login/$', views.login, name='login'),

	url(r'^logout/$', auth_views.logout, name='logout', 
		kwargs={'next_page': settings.LOGIN_URL}),

	url(r'^profile/$', views.profile, name='profile'),
	url(r'^profile_edit/$', views.profile_edit, name='profile_edit'),

	url(r'^password_edit/$', views.password_edit, name='password_edit'),
	url(r'^like/$', views.like_list, name='like_list'),
	url(r'^cart/$', views.cart_list, name='cart_list'),
	url(r'^orderlist/$', views.order_list, name='order_list'),
	url(r'^productlist/$', views.product_list, name='product_list'),
]