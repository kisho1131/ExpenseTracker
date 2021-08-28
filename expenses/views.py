from django.contrib import messages
from django.core import paginator
from .models import Category, Expense
from django.contrib.auth import logout
from django.shortcuts import redirect, render, resolve_url
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from preferences.models import UserPreference
import json
import datetime
# Create your views here.


@login_required(login_url='/authentication/login')
def Index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner = request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency  = UserPreference.objects.get(user = request.user).currency
    context = {
        'expenses' : expenses,
        'page_obj' :page_obj,
        'currency' : currency, 
    }
    return render(request, 'expenses/index.html', context=context)


def Add_Expenses(request):

    categories = Category.objects.all()
    context ={
        'categories' : categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add-expenses.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, "Amount is Required !!")
            return render(request, 'expenses/add-expenses.html', context)
        description = request.POST['description']
        if not description:
            messages.error(request, "Description is Required !!")
            return render(request, 'expenses/add-expenses.html', context)
        category = request.POST.get('category')
        date = request.POST['date']
        
        Expense.objects.create(owner= request.user, amount=amount, date = date, category=category, description=description)
        messages.success(request, "Expense Saved Successfully !!")
        return redirect('expenses')


def Edit_Expenses(request, id):
    categories = Category.objects.all()
    expense = Expense.objects.get(pk = id)
    context = {
            'categories' : categories,
            'expense' :expense,
            'values' : expense,
        }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    

    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, "Amount is Required !!")
            return render(request, 'expenses/edit-expenses.html', context)
        description = request.POST['description']
        if not description:
            messages.error(request, "Description is Required !!")
            return render(request, 'expenses/edit-expense.html', context)
        category = request.POST.get('category')
        date = request.POST.get('date')
        
        # Expense.objects.create(owner= request.user, amount=amount, date = date, category=category, description=description)
        expense.owner= request.user
        expense.amount=amount
        expense.date = date
        expense.category=category
        expense.description=description
        expense.save()
        messages.success(request, "Expense Updated Successfully !!")
        return redirect('expenses')


def Delete_Expenses(request, id):
    expense =Expense.objects.get(pk = id)
    expense.delete()
    messages.success(request, "Expense Deleted Successfully !!")
    return redirect ('expenses')
    

def Search_Expenses(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        search_str = data['search']
        
        expenses = Expense.objects.filter(amount__istartswith=search_str, owner = request.user) | Expense.objects.filter(date__istartswith=search_str, owner = request.user) | Expense.objects.filter(description__icontains=search_str, owner = request.user) | Expense.objects.filter(category__icontains=search_str, owner = request.user)
    data  = expenses.values()
    return JsonResponse(list(data), safe = False)


def Expense_Category_Summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def Stats_View(request):
    return render(request, 'expenses/stats.html')