from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'expenses'),
    path('addExpenses', views.addExpense, name = "addExpense"),
]
