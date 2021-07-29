from django.contrib import messages
from django.core import paginator
from .models import Category, Expense
from django.contrib.auth import logout
from django.shortcuts import redirect, render, resolve_url
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
# Create your views here.

@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner = request.user)
    paginator = Paginator(expenses, 3)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {

        'expenses' : expenses,
        'page_obj' :page_obj
    }
    return render(request, 'expenses/index.html', context=context)

def addExpense(request):

    categories = Category.objects.all()
    context ={
        'categories' : categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/addExpenses.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, "Amount is Required !!")
            return render(request, 'expenses/addExpenses.html', context)
        description = request.POST['description']
        if not description:
            messages.error(request, "Description is Required !!")
            return render(request, 'expenses/addExpenses.html', context)
        category = request.POST.get('category')
        date = request.POST['date']
        
        Expense.objects.create(owner= request.user, amount=amount, date = date, category=category, description=description)
        messages.success(request, "Expense Saved Successfully !!")
        return redirect('expenses')



def expense_edit(request, id):
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


def delete_expense(request, id):
    expense =Expense.objects.get(pk = id)
    expense.delete()
    messages.success(request, "Expense Deleted Successfully !!")
    return redirect ('expenses')
    

def search_expenses(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        search_str = data['search']

        expenses = Expense.objects.filter(amount__istartswith=search_str, owner = request.user) | Expense.objects.filter(date__istartswith=search_str, owner = request.user) | Expense.objects.filter(description__icontains=search_str, owner = request.user) | Expense.objects.filter(category__icontains=search_str, owner = request.user)
    data  = expenses.values()
    return JsonResponse(list(data), safe = False)

