from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'expenses'),
    path('addExpenses', views.addExpense, name = "addExpense"),
    path('edit-expense/<int:id>', views.expense_edit, name = "edit-expense"),
    path('delete-expense/<int:id>', views.delete_expense, name = 'delete-expense'),
]
