from django.contrib import admin
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.Index, name = 'income'),
    path('add-income', views.Add_Income, name = "add-income"),
    path('edit-income/<int:id>', views.Edit_Income, name = "edit-income"),
    path('delete-income/<int:id>', views.Delete_Income, name = 'delete-income'),
    path('search-income', csrf_exempt(views.Search_Income), name = "search-income"),
]
