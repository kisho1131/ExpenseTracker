from django.shortcuts import render
from django.views import View
# Create your views here.

class RegistrationView(View):
    def get(self, requerts):
        return render(requerts, 'authentication/register.html')

