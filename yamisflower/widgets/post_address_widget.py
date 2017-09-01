import re
from django import forms
from django.template.loader import render_to_string
from django.conf import settings


class PostAddressWidget(forms.TextInput):

	def render(self, name, value, attrs):

		html = render_to_string('widgets/post_address_widget.html')

		attrs['style']='width:7rem;margin-right:2rem;'
		attrs['readonly'] = 'readonly'

		parent_html = super().render(name, value, attrs)

		return parent_html+html