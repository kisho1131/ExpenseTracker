from .models import Category, Expense
from django.contrib import admin

# Register your models here.

admin.site.register(Expense)
admin.site.register(Category)