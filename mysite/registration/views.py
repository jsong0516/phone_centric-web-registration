from django.shortcuts import render,loader
from django.http import HttpResponse

# Create your views here.

def index(request):
	template = loader.get_template('registration/index.html')
	return HttpResponse(template.render())
    #return HttpResponse("Hello, world. You're at the Registation index.")

def courselist(request):
	template = loader.get_template('registration/courselist.html')
	return HttpResponse(template.render())
    #return HttpResponse("Hello, world. You're at the Registation index.")

def handleSubmit(request):
	print "HIHIHIHI"