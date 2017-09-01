from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.flower_list, name="flower_list"),
	url(r'^(?P<id>\d+)/$', views.flower_detail, name="flower_detail"),
	url(r'^order/(?P<numbers>[\d/]+)/$', views.flower_order, name="flower_order"),
	url(r'^(?P<id>\d+)/like/$', views.flower_like, name="flower_like"),
	url(r'^(?P<id>\d+)/cart_add/$', views.flower_cart_add, name="flower_cart_add"),
	url(r'^cart_delete/(?P<numbers>[\d/]+)/$', views.flower_cart_delete, name="flower_cart_delete"),
	url(r'^order_new/$', views.order_new, name="order_new"),

	url(r'^(?P<flower_id>\d+)/review/new$', views.review_new, name="review_new"),
	url(r'^(?P<flower_id>\d+)/review/(?P<pk>\d+)/edit$', views.review_edit, name="review_edit"),
	url(r'^review/delete/$', views.review_delete, name="review_delete"),
	url(r'^(?P<flower_id>\d+)/commentqa/new$', views.commentqa_new, name="commentqa_new"),
	url(r'^(?P<flower_id>\d+)/commentqa/(?P<pk>\d+)/edit$', views.commentqa_edit, name="commentqa_edit"),
	url(r'^commentqa/delete/$', views.commentqa_delete, name="commentqa_delete"),

	url(r'^rereview/new/$', views.rereview_new, name="rereview_new"),
	url(r'^rereview/edit/$', views.rereview_edit, name="rereview_edit"),
	url(r'^rereview/delete/$', views.rereview_delete, name="rereview_delete"),
	url(r'^recommentqa/new/$', views.recommentqa_new, name="recommentqa_new"),
	url(r'^recommentqa/edit/$', views.recommentqa_edit, name="recommentqa_edit"),
	url(r'^recommentqa/delete/$', views.recommentqa_delete, name="recommentqa_delete"),

	url(r'^manager/$', views.mflower_list, name='mflower_list'),
	url(r'^manager/new/$', views.mflower_new, name='mflower_new'),
	url(r'^manager/(?P<id>\d+)/edit/$', views.mflower_update, name='mflower_update'),
	url(r'^manager/mflower_delete/$', views.mflower_delete, name='mflower_delete'),
	url(r'^manager/mflower_is_best/$', views.mflower_is_best, name='mflower_is_best'),
]