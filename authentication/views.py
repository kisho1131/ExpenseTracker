from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
import json


# Create your views here
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        #get user data
        #Validate
        #Create Account
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'fieldValues' : request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(password) < 6:
                    messages.error(request, "Password Too Short !!")
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create_user(username= username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                emailSubject = "Active Your Account"
                emailBody = "Testing the Email!! Stay Online !! "
                email = EmailMessage(
                    emailSubject,
                    emailBody,
                    'webtrills.india@gmail.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, "Account Created Successfully !!")
                return render(request, 'authentication/register.html')
        return render(request, 'authentication/register.html')


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error' : 'Username should only contain Alphanumeric [(a-z)(A-Z)(0-9)] Characters'}, status = 400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error' : 'Sorry!! username is Already Taken | Choose Another'}, status = 409)

        return JsonResponse({'username_valid':True})

# Email Validation 
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error' : 'Enter Valid Email ID'}, status = 400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error' : 'Sorry!! Email is in Use'}, status = 409)

        return JsonResponse({'email_valid':True})