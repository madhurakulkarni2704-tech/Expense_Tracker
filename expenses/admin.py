from django.contrib import admin
from .models import Expense, Category, Profile

admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(Profile)
