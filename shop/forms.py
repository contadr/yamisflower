from django import forms
from django.forms import ValidationError
from .models import Flower, Review, Commentqa


class mFlowerForm(forms.ModelForm):

	class Meta:
		model = Flower
		fields = ('name', 'description', 'price', 'thumbnail', 'image01','image02','image03','image04','image05',)

	# def save(self):
	# 	flower = super().save()
	# 여기서 확인한담에 7이면 다시 내림


class ReviewForm(forms.ModelForm):

	class Meta:
		model = Review
		fields = ('subject', 'content', 'image01', 'image02',)


class CommentqaForm(forms.ModelForm):

	class Meta:
		model = Commentqa
		fields = ('subject', 'content', 'image01', 'image02',)