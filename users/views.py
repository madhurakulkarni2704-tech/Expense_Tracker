# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm  # make sure this form exists

# ------------------ REGISTER VIEW ------------------ #
def register(request):
    """
    Handles new user registration.
    Uses your CustomUserCreationForm to create users safely.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after registration
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('dashboard')  # go to dashboard after signup
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


# ------------------ LOGIN VIEW ------------------ #
def user_login(request):
    """
    Authenticates users using Django's built-in AuthenticationForm.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')  # go to dashboard after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


# ------------------ LOGOUT VIEW ------------------ #
def user_logout(request):
    """
    Logs out the current user and redirects to login page.
    """
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')
