from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Source, UserIncome
from django.core.paginator import Paginator
from preferences.models import UserPreference
import json
# Create your views here.


@login_required(login_url='/authentication/login')
def Index(request):
    sources = Source.objects.all()
    income = UserIncome.objects.filter(owner = request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency  = UserPreference.objects.get(user = request.user).currency
    context = {
        'income' : income,
        'page_obj' :page_obj,
        'currency' : currency, 
    }
    return render(request, 'income/index.html', context=context)


@login_required(login_url='/authentication/login')
def Add_Income(request):
    sources = Source.objects.all()
    context ={
        'sources' : sources,
        'values': request.POST
    }

    if request.method == 'GET':                     
        return render(request, 'income/add-income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, "Amount is Required !!")
            return render(request, 'income/add-income.html', context)
        description = request.POST['description']
        if not description:
            messages.error(request, "Description is Required !!")
            return render(request, 'income/add-income.html', context)
        sources = request.POST.get('source')
        date = request.POST['date']
        
        UserIncome.objects.create(owner= request.user, amount=amount, date = date, source=sources, description=description)
        messages.success(request, "Record Saved Successfully !!")
        return redirect('income')


def Edit_Income(request, id):
    sources = Source.objects.all()
    income = UserIncome.objects.get(pk = id)
    context = {
            'sources' : sources,
            'income' :income,
            'values' : income,
        }
    if request.method == 'GET':
        return render(request, 'income/edit-income.html', context)
    

    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, "Amount is Required !!")
            return render(request, 'income/edit-income.html', context)
        description = request.POST['description']
        if not description:
            messages.error(request, "Description is Required !!")
            return render(request, 'income/edit-income.html', context)
        sources = request.POST.get('source')
        date = request.POST.get('date')
        
        # Expense.objects.create(owner= request.user, amount=amount, date = date, category=category, description=description)
        income.amount=amount
        income.date = date
        income.owner= request.user
        income.source=sources
        income.description=description
        income.save()
        messages.success(request, "Expense Updated Successfully !!")
        return redirect('income')


def Delete_Income(request, id):
    income =UserIncome.objects.get(pk = id)
    income.delete()
    messages.success(request, "Expense Deleted Successfully !!")
    return redirect ('income')


def Search_Income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('search')
        
        income = UserIncome.objects.filter(amount__istartswith=search_str, owner = request.user) | UserIncome.objects.filter(date__istartswith=search_str, owner = request.user) | UserIncome.objects.filter(description__icontains=search_str, owner = request.user) | UserIncome.objects.filter(source__icontains=search_str, owner = request.user)
    data  = income.values()
    return JsonResponse(list(data), safe = False)