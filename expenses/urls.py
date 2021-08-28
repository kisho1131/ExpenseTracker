from django.contrib import admin
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.Index, name = 'expenses'),
    path('add-expense', views.Add_Expenses, name = "add-expenses"),
    path('edit-expense/<int:id>', views.Edit_Expenses, name = "edit-expense"),
    path('delete-expense/<int:id>', views.Delete_Expenses, name = 'delete-expense'),
    path('search-expenses', csrf_exempt(views.Search_Expenses), name = "search-expense"),
    path('expense-category-summary', views.Expense_Category_Summary, name = 'expense-category-summary'),
    path('stats', views.Stats_View, name = 'stats'),
]
