from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
# from django.core.validators import validate_email
from validate_email import validate_email


# Create your views here.

class RegistrationView(View):
    def get(self, requerts):
        return render(requerts, 'authentication/register.html')

class UsernameValidationView(View):
    def post(self, requests):
        data = json.loads(requests.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error' : 'Username should only contain Alphanumeric [(a-z)(A-Z)(0-9)] Characters'}, status = 400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error' : 'Sorry!! username is Already Taken | Choose Another'}, status = 409)

        return JsonResponse({'username_valid':True})

# Email Validation 
class EmailValidationView(View):
    def post(self, requests):
        data = json.loads(requests.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error' : 'Enter Valid Email ID'}, status = 400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error' : 'Sorry!! Email is in Use'}, status = 409)

        return JsonResponse({'email_valid':True})