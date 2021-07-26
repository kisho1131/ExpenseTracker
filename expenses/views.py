from django.contrib.auth import logout
from django.http import response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/authentication/login')
def index(requests):
    return render(requests, 'expenses/index.html')

def addExpense(requests):
    return render(requests, 'expenses/addExpenses.html')