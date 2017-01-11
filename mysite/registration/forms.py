from django import forms
from django.forms import ModelForm


class RegistrationForm(forms.Form):
	# There are a several approaches for this. We can generate form using this or just use my html
	# I used html template form first so, I just sticked with it
	name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'name'}))
	phone = forms.CharField(widget=forms.TextInput(attrs={'id' : 'phone'}))
	course = forms.CharField(widget=forms.TextInput(attrs={'id' : 'course'}))
	