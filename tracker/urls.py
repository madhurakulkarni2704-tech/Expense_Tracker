from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('register')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root URL
    path('', home_redirect, name='home'),

    # Users app (register, login, logout, password reset)
    path('users/', include('users.urls')),

    # Expenses app (dashboard, add_expense, list, etc.)
    path('expenses/', include('expenses.urls')),
]
