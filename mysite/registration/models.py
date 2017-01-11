from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm

class Registration(models.Model):
	name = models.CharField(max_length=100)
	phone = models.CharField(max_length=100)
	course = models.CharField(max_length=100)

# Create your models here.
class RegistrationForm(ModelForm):
	class Meta:
		model = Registration
		fields = ['name', 'phone', 'course']