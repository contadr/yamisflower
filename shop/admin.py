from django.contrib import admin
from .models import Flower, FloImg, Like, Cart, Order, Product, Review, Commentqa, Rereview, Recommentqa


@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'is_best']
	list_display_links = ['id', 'name']
	list_editable = ['is_best']

@admin.register(FloImg)
class FloImgAdmin(admin.ModelAdmin):
	list_display = ['id', 'flower_id']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
	list_display = ['user', 'flower']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ['user', 'flower']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['user', 'order_code', 'created_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['order', 'flower', 'count']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ['subject', 'author']

@admin.register(Commentqa)
class CommentqaAdmin(admin.ModelAdmin):
	list_display = ['subject', 'author']

@admin.register(Rereview)
class RereviewAdmin(admin.ModelAdmin):
	list_display = ['id', 'content']
	list_display_links = ['content']

@admin.register(Recommentqa)
class RecommentqaAdmin(admin.ModelAdmin):
	list_display = ['id', 'content']
	list_display_links = ['content']