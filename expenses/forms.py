# expenses/forms.py
from django import forms
from .models import Expense, Budget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# ---------------- Expense Form ---------------- #
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'date', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter expense title'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount',
                'step': '0.01'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional description'
            }),
        }

# ---------------- Budget Form ---------------- #
class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['month', 'amount', 'category']
        widgets = {
            'month': forms.DateInput(attrs={
                'type': 'month',
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

# ---------------- User Registration Form ---------------- #
#8 nov 2025 new 
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        }
