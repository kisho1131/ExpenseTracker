from django.contrib import messages
from django.shortcuts import render
from django.conf import settings
from .models import UserPreference
import os
import json
# Create your views here.

def index(request):
    
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open (file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value':v })

    exists = UserPreference.objects.filter(user = request.user).exists()
    userpreferences = None
    if exists:
        userpreferences= UserPreference.objects.get(user = request.user)


    if request.method == 'GET':
        return render(request, 'preferences/index.html', {'currencies' : currency_data,  'userpreferences' : userpreferences})
    
    else:
        currency = request.POST['currency']
        if exists:
            userpreferences.currency = currency
            userpreferences.save()
        else:
            UserPreference.objects.create(user= request.user, currency = currency)
        messages.success(request, " Preferred Currency Saved :)")
        return render(request, 'preferences/index.html', {'currencies' : currency_data, 'userpreferences' : userpreferences})

