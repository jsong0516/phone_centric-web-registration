from django.shortcuts import render,loader
from django.http import HttpResponse
from django.template import RequestContext

# For registering a model and handling post request
from models import Registration
from models import RegistrationForm
from django.views.decorators.csrf import csrf_exempt

# SMS
from random import randint
import sms

@csrf_exempt
def index(request):
	print "index is called"
	if request.method == 'POST':
		return get_form(request)

	template = loader.get_template('registration/index.html')
	return HttpResponse(template.render())

@csrf_exempt
def retrieve(request):
	print "retrieve is called"
	template = loader.get_template('registration/retrieve.html')
	return HttpResponse(template.render())


def get_form(request):
    # if this is a POST request we need to process the form data
    # print request.POST['name']
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        
        # Generate a random number
        rand = randint(1000, 9999)
        
        
        # Hope this is not cheating
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['auth'] = str(rand)
        request.POST._mutable = mutable


        form = RegistrationForm(request.POST)
        print "Form"
        print form
        # print form['name']['value']
        # check whether it's valid:
        if form.is_valid():


            instance = form.save()



            return HttpResponse('Thank you! You will receive a text message soon.')
        # return HttpResponse('Thank you! You will receive a text message soon.')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegistrationForm()

    return render(request, 'index.html', {'form': form})