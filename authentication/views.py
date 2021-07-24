from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
# Create your views here.

class RegistrationView(View):
    def get(self, requerts):
        return render(requerts, 'authentication/register.html')

class UsernameValidationView(View):
    def post(self, requests):
        data = json.loads(requests.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error' : 'username should only contain alphanumeric characters'}, status = 400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error' : 'Sorry!! username is Already Taken Choose Another'}, status = 409)

        return JsonResponse({'username_valid':True})
