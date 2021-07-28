from django.contrib import messages
from .models import Category, Expense
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner = request.user)
    context = {
        'expenses' : expenses
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


    
