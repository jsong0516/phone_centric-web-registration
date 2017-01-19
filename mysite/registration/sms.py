from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

account_sid = "ACcf72078104093e8242bacfc95d4bb7c6" # Your Account SID from www.twilio.com/console
auth_token  = "0418a58a68a4ba02b423406ea42b5421"  # Your Auth Token from www.twilio.com/console

def sendSMS(toNumber, sms):

	client = TwilioRestClient(account_sid, auth_token)
	try:
		message = client.messages.create(body= "Thank you very much for registration! Your number is " + str(sms),
		    to=toNumber,    # Replace with your phone number
		    from_="+12136746361") # Replace with your Twilio number
		return (True, "")
	except TwilioRestException as e:
		print e
		return (False, e)