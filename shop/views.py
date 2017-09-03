import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, QueryDict, JsonResponse
from django.contrib import messages
from accounts.models import Profile
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Flower, Like, Cart, Order, Product, Review, Commentqa, Rereview, Recommentqa
from .forms import mFlowerForm, ReviewForm, CommentqaForm


class FlowerListView(ListView):
	model = Flower

	def get_context_data(self):
		context = super().get_context_data()
		context['isbestcount'] = Flower.objects.filter(is_best=True).count()
		return context

flower_list = FlowerListView.as_view()


def flower_detail(request, id):
	flower = get_object_or_404(Flower, id=id)

	review_list = Review.objects.filter(flower_id=id).select_related('author').select_related('rereview')
	paginator = Paginator(review_list, 5)
	page = request.GET.get('page1')
	try:
		reviews = paginator.page(page)
	except PageNotAnInteger:
		reviews = paginator.page(1)
	except EmptyPage:
		reviews = paginator.page(paginator.num_pages)

	commentqa_list = Commentqa.objects.filter(flower_id=id).select_related('author').select_related('recommentqa')
	paginator = Paginator(commentqa_list, 5)
	page = request.GET.get('page2')
	try:
		commentqas = paginator.page(page)
	except PageNotAnInteger:
		commentqas = paginator.page(1)
	except EmptyPage:
		commentqas = paginator.page(paginator.num_pages)

	if Like.objects.filter(user_id=request.user.id, flower_id=id):
		like = '<span class="glyphicon glyphicon-heart" aria-hidden="true"></span>'
	else:
		like = '<span class="glyphicon glyphicon-heart-empty" aria-hidden="true"></span>'

	return render(request, 'shop/flower_detail.html', {
		'like': like,
		'flower': flower,
		'review_list': reviews,
		'commentqa_list': commentqas,
	})



@login_required
def flower_order(request, numbers):
	result = list(map(lambda s: int(s or 0), numbers.split('/')))
	flower_list = Flower.objects.filter(pk__in=result)

	profile = Profile.objects.filter(user_id=request.user.id).values()
	if not list(profile)[0]['post_code'] or not list(profile)[0]['address']or not list(profile)[0]['address_detail']:
		messages.warning(request, "하단의 \'기본정보 변경\'을 눌러 배송지 주소를 등록해주세요.")
		return render(request, 'accounts/profile.html')
	return render(request, 'shop/flower_order.html', {
		'flower_list': flower_list,
	})


def flower_cart_add(request, id):
	if request.method == 'POST':

		if request.user.is_authenticated():
			Cart.objects.create(
				user_id = request.user.id,
				flower_id = id,
			)
			return HttpResponse(1)
		else:
			return HttpResponse(0)


@login_required
def flower_cart_delete(request, numbers):
	if request.method == 'POST':
		result = list(map(lambda s: int(s or 0), numbers.split('/')))
		cart = Cart.objects.filter(id__in=result)
		cart.delete()
		return HttpResponse(1)


def flower_like(request, id):
	if request.method == 'POST':

		if request.user.is_authenticated():
			if Like.objects.filter(user_id=request.user.id, flower_id=id):
				like = Like.objects.filter(user_id=request.user.id, flower_id=id)
				like.delete()
				return HttpResponse(0)
			else:
				Like.objects.create(
					user_id = request.user.id, # 위에 super().save()로 받아온 user 인스턴스
					flower_id = id,
				)
				return HttpResponse(1)
		else:
			return HttpResponse(2)


@login_required
def order_new(request):
	if request.method == 'POST':
		body = QueryDict(request.body)

		flowers = request.POST.getlist('flower_id[]')
		counts = request.POST.getlist('flower_count[]')

		order = Order.objects.create(
			user_id = request.user.id,
			receiver_name = body.get("receiver_name"),
			receiver_phone_number = body.get("receiver_phone_number"),
			receiver_email = body.get("receiver_email"),
			receiver_post_code = body.get("receiver_post_code"),
			receiver_address = body.get("receiver_address"),
			receiver_address_detail = body.get("receiver_address_detail"),
			pay_type = body.get("pay_type"),
			total_price = body.get("total_price"),
		)

		for i in range(0, len(flowers)):
			Product.objects.create(
				order = order,
				flower_id = flowers[i],
				count = counts[i],
			)

		messages.success(request, '상품 주문 완료. 감사합니다.')
		return HttpResponse(1)


@login_required
def review_new(request, flower_id):
	flower = get_object_or_404(Flower, pk=flower_id)

	if request.method == 'POST':
		form = ReviewForm(request.POST, request.FILES)
		if form.is_valid():
			review = form.save(commit=False)
			review.flower = flower
			review.author = request.user
			review.save()
			return redirect('shop:flower_detail', flower.pk)
	else:
		form = ReviewForm()
	return render(request, 'shop/review_form.html', {
		'form' : form,
		'flower': flower,
	})


@login_required
def review_edit(request, flower_id, pk):
	flower = get_object_or_404(Flower, pk=flower_id)
	review = get_object_or_404(Review, pk=pk)

	if review.author != request.user:
		return redirect(review.flower)

	if request.method == 'POST':
		form = ReviewForm(request.POST, request.FILES, instance=review)
		if form.is_valid():
			review = form.save()
			return redirect(review.flower)
	else:
		form = ReviewForm(instance=review)
	return render(request, 'shop/review_form.html', {
		'form' : form,
		'flower': flower,
	})

@login_required
def review_delete(request):
	if request.method == 'DELETE':
		review = Review.objects.get(id=int(QueryDict(request.body).get('review_id')))
		review.delete()
		return HttpResponse(1)
	else:
		return HttpResponse(0)


@login_required
def commentqa_new(request, flower_id):
	flower = get_object_or_404(Flower, pk=flower_id)

	if request.method == 'POST':
		form = CommentqaForm(request.POST, request.FILES)
		if form.is_valid():
			commentqa = form.save(commit=False)
			commentqa.flower = flower
			commentqa.author = request.user
			commentqa.save()
			return redirect('shop:flower_detail', flower.pk)
	else:
		form = CommentqaForm()
	return render(request, 'shop/commentqa_form.html', {
		'form' : form,
		'flower': flower,
	})


@login_required
def commentqa_edit(request, flower_id, pk):
	flower = get_object_or_404(Flower, pk=flower_id)
	commentqa = get_object_or_404(Commentqa, pk=pk)

	if commentqa.author != request.user:
		return redirect(commentqa.flower)

	if request.method == 'POST':
		form = CommentqaForm(request.POST, request.FILES, instance=commentqa)
		if form.is_valid():
			commentqa = form.save()
			return redirect(commentqa.flower)
	else:
		form = CommentqaForm(instance=commentqa)
	return render(request, 'shop/commentqa_form.html', {
		'form' : form,
		'flower': flower,
	})


@login_required
def commentqa_delete(request):
	if request.method == 'DELETE':
		commentqa = Commentqa.objects.get(id=int(QueryDict(request.body).get('commentqa_id')))
		commentqa.delete()
		return HttpResponse(1)
	else:
		return HttpResponse(0)


@staff_member_required
def rereview_new(request):
	if request.method == 'POST':
		Rereview.objects.create(
			user_id = request.user.id,
			review_id = request.POST.get("review_id"),
			content = request.POST.get("content"),
		)

		return HttpResponse(1)


@staff_member_required
def rereview_edit(request):
	if request.method == 'POST':

		rereview = Rereview.objects.get(review_id=request.POST.get("review_id"))
		rereview.content = request.POST.get("content")
		rereview.save()

		return HttpResponse(1)


@staff_member_required
def rereview_delete(request):
	if request.method == 'POST':

		rereview = Rereview.objects.get(id=request.POST.get("rereview_id"))
		rereview.delete()

		return HttpResponse(1)


@staff_member_required
def recommentqa_new(request):
	if request.method == 'POST':
		Recommentqa.objects.create(
			user_id = request.user.id,
			commentqa_id = request.POST.get("commentqa_id"),
			content = request.POST.get("content"),
		)
		
		return HttpResponse(1)


@staff_member_required
def recommentqa_edit(request):
	if request.method == 'POST':

		recommentqa = Recommentqa.objects.get(commentqa_id=request.POST.get("commentqa_id"))
		recommentqa.content = request.POST.get("content")
		recommentqa.save()

		return HttpResponse(1)


@staff_member_required
def recommentqa_delete(request):
	if request.method == 'POST':

		recommentqa = Recommentqa.objects.get(id=request.POST.get("recommentqa_id"))
		recommentqa.delete()

		return HttpResponse(1)


#################################################################
#################################################################
############### 	ONLY 			#############################
############### 	MANAGER 		#############################
############### 	VIEW 			#############################
#################################################################
#################################################################


@staff_member_required
def mflower_list(request):
	flower_list = Flower.objects.all()
	return render(request, 'shop/mflower_list.html', {
		'flower_list': flower_list,
	})


@staff_member_required
def mflower_new(request):
	if request.method == 'POST':
		form = mFlowerForm(request.POST, request.FILES)
		if form.is_valid():
			flower = form.save()
			messages.success(request, '\'{}\' 이 등록되었습니다.'.format(flower))
			return redirect(flower)
	else:
		form = mFlowerForm()
	return render(request, 'shop/mflower_form.html', {
		'form' : form,
	})

@staff_member_required
def mflower_update(request, id):
	flower = get_object_or_404(Flower, id=id)

	if request.method == 'POST':
		form = mFlowerForm(request.POST, request.FILES, instance=flower)
		if form.is_valid():
			flower = form.save()
			messages.success(request, '\'{}\' 의 정보를 수정하였습니다.'.format(flower))
			return redirect(flower) # post.get_absolute_url => post_detail.html
	else:
		form = mFlowerForm(instance=flower)
	return render(request, 'shop/mflower_form.html', {
		'form' : form,
	})

@staff_member_required
def mflower_delete(request):
	if request.method == 'DELETE':
		flower = Flower.objects.get(id=int(QueryDict(request.body).get('flower_id')))
		flower.delete()
		return HttpResponse(1)
	else:
		return HttpResponse(0)


@staff_member_required
def mflower_is_best(request):
	if request.method == 'POST':
		body = QueryDict(request.body)

		if int(body.get('is_best')) == 1:
			if Flower.objects.filter(is_best=1).count() >= 6:
				return HttpResponse(0)
			else:
				Flower.objects.filter(id=int(body.get('flower_id'))).update(is_best=int(body.get('is_best')))
				return HttpResponse(1)
		else:
			Flower.objects.filter(id=int(body.get('flower_id'))).update(is_best=int(body.get('is_best')))
			return HttpResponse(2)
