from django.conf.urls import url
from . import views, forms

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^retrieve', views.retrieve, name='retrieve'),
    url(r'^$', forms.RegistrationForm, name='RegistrationForm'),
]