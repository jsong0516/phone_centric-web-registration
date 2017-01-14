from django.shortcuts import render,loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

# For registering a model and handling post request
from models import Registration
from models import RegistrationForm
from django.views.decorators.csrf import csrf_exempt

# SMS
from random import randint
from sms import sendSMS

STARTING_NUMBER = 1000
ENDING_NUMBER = 9999

@csrf_exempt
def index(request):
	print "index is called"
	print request
	if request.method == 'POST':
		return get_form(request)

	template = loader.get_template('registration/index.html')
	return HttpResponse(template.render())

@csrf_exempt
def retrieve(request):
	print "retrieve is called"
	print request

	if request.method == 'GET':
		return ret_form(request)

	template = loader.get_template('registration/index.html')
	return HttpResponse(template.render())

def ret_form(request):
	c_phone = request.GET['phone']
	c_auth = request.GET['auth']

	# encode 
	c_auth_ascii = c_auth.encode("ascii")

	# if auth is invalid then, it should display the info
	if c_auth is None or c_auth == ''or  (int(c_auth) > ENDING_NUMBER and int(c_auth) < STARTING_NUMBER):
		entry = Registration.objects.filter(phone=c_phone)
		if(len(entry) <= 0):
			return HttpResponse('No phone number found. Please re-enter')

		correct_auth_code = entry[0].auth
		sendSMS(c_phone, correct_auth_code)
		return HttpResponse('Auth is invalid. Sent Auth code again')

	result = Registration.objects.filter(phone=c_phone, auth=c_auth_ascii)

	if(len(result) <= 0):
		return HttpResponse('No Match')

	result_str = "Name : " + str(result[0].name) + "<br />"
	result_str += "Phone : " + str(result[0].phone) + "<br />"
	result_str += "Course : "
	for entry in result:
		result_str += str(result[0].course) + "<br />"
	return HttpResponse(result_str)

def get_form(request):
    # if this is a POST request we need to process the form data
    # print request.POST['name']
    if request.method == 'POST':

    	# if the phone number is already exist, then remove it.
    	Registration.objects.filter(phone=request.POST['phone']).delete()

        # create a form instance and populate it with data from the request:
        # Generate a random number
        rand = randint(STARTING_NUMBER, ENDING_NUMBER)
        
        # Make request as mutable
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['auth'] = str(rand)
        request.POST._mutable = mutable
        form = RegistrationForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            print "Registration is completed: "
            print "Name : " + request.POST['name']
            print "Phone : " + request.POST['phone']
            print "Course : " + request.POST['course']
            print "Auth : " + request.POST['auth']
            instance = form.save()
            sendSMS(request.POST['phone'], rand)
            template = loader.get_template('registration/index.html')
            return HttpResponse("Registration is completed. You will receive SMS message shortly")
        # return HttpResponse('Thank you! You will receive a text message soon.')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegistrationForm()

    return render(request, 'index.html', {'form': form})