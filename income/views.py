from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Source, UserIncome
from django.core.paginator import Paginator
from preferences.models import UserPreference

# Create your views here.


@login_required(login_url='/authentication/login')
def index(request):
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
def addIncome(request):
    sources = Source.objects.all()
    context ={
        'source' : sources,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'income/add-income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, "Amount is Required !!")
            return render(request, 'income/addIncome.html', context)
        description = request.POST['description']
        if not description:
            messages.error(request, "Description is Required !!")
            return render(request, 'income/addIncome.html', context)
        sources = request.POST.get('sources')
        date = request.POST['date']
        
        UserIncome.objects.create(owner= request.user, amount=amount, date = date, sources=sources, description=description)
        messages.success(request, "Record Saved Successfully !!")
        return redirect('income')
