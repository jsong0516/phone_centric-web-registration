from django.shortcuts import render,loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext

# For registering a model and handling post request
from models import Registration
from models import RegistrationForm
from django.views.decorators.csrf import csrf_exempt

# SMS
from random import randint
from sms import sendSMS

STARTING_NUMBER = 1000
ENDING_NUMBER = 9999

template = loader.get_template('registration/index.html')

@csrf_exempt
def index(request):
	if request.method == 'POST':
		return get_form(request)
	context = Context({"ret": "", "reg" : "active", "alert" : False})
	return HttpResponse(template.render(context))

@csrf_exempt
def retrieve(request):
	if request.method == 'GET':
		return ret_form(request)
	context = Context({"ret": "active", "reg" : "", "alert" : False})
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
			context = Context({"ret": "active", "reg" : "", "alert_body" : "No phone number found. Please re-enter your phone number", "alert" : True})
			return HttpResponse(template.render(context))
		correct_auth_code = entry[0].auth
		sendSMS(c_phone, correct_auth_code)
		context = Context({"ret": "active", "reg" : "", "alert_body" : "Authentication is invalid. We will send Authentication code again if phone number is valid", "alert" : True})
		return HttpResponse(template.render(context))

	result = Registration.objects.filter(phone=c_phone, auth=c_auth_ascii)

	if(len(result) <= 0):
		context = Context({"ret": "active", "reg" : "", "alert_body" : "No Match", "alert" : True})
		return HttpResponse(template.render(context))

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
            print "Name : " + request.POST['name']
            print "Phone : " + request.POST['phone']
            print "Course : " + request.POST['course']
            print "Auth : " + request.POST['auth']
            SMSResult = sendSMS(request.POST['phone'], rand)
            context = None
            instance = None
            if not SMSResult[0]: # if it is false
            	# if phone number is incorrect, then, need to re-register
            	print "SMS failed"
            	body = "Registration is incomplete. SMS is not sent correctly"
            	context = Context({"ret": "", "reg" : "active", "alert_body" : body, "alert" : True})
            else:
            	print "SMS pass"
            	instance = form.save()
            	body = "Registration is completed. You will receive SMS message shortly"
            	context = Context({"ret": "active", "reg" : "", "alert_body" : body, "alert" : True})
            return HttpResponse(template.render(context))
    else:
        form = RegistrationForm()

    return render(request, 'index.html', {'form': form})
