from django.http import response
from django.shortcuts import render

# Create your views here.

def index(requests):
    return render(requests, 'expenses/index.html')

def addExpense(requests):
    return render(requests, 'expenses/addExpenses.html')