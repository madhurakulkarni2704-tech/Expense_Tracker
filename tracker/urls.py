from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Optional: simple home page
def home(request):
    return redirect('register')  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # include the users app
    path('', home),  # root URL, you can later redirect to register page
    path('', include('expenses.urls')), 
    # path('accounts/', include('django.contrib.auth.urls')),

]
