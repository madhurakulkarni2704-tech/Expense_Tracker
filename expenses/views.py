# expenses/views.py
import json
import csv
from datetime import date
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login
from .models import Expense, Category, Budget
from .forms import ExpenseForm, BudgetForm, RegisterForm

# ------------------------
# User Registration new 9 nov
# ------------------------
"""def register_view(request):
    #Handles user signup.
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in
            messages.success(request, f"Welcome {user.username}! Your account has been created.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

"""
# ------------------------
# Dashboard View
# ------------------------
@login_required
def dashboard(request):
    user = request.user
    qs = Expense.objects.filter(user=user)

    # Overall total
    overall = qs.aggregate(total=Sum('amount'))['total'] or 0

    # Category breakdown
    cat_qs = qs.values('category__name').annotate(total=Sum('amount')).order_by('-total')
    categories = [c['category__name'] or 'Uncategorized' for c in cat_qs]
    category_amounts = [float(c['total'] or 0) for c in cat_qs]

    # Last N months
    months_back = int(request.GET.get('months', 6))
    end_month = date.today().replace(day=1)
    start_month = end_month - relativedelta(months=months_back - 1)

    monthly_qs = (
        qs.filter(date__gte=start_month)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    # Continuous timeline mapping
    totals_map = {}
    for m in monthly_qs:
        month_dt = m['month'].date() if hasattr(m['month'], 'date') else m['month']
        month_dt = month_dt.replace(day=1)
        totals_map[month_dt] = float(m['total'] or 0)

    month_labels, month_totals = [], []
    cur = start_month
    while cur <= end_month:
        month_labels.append(cur.strftime('%b %Y'))
        month_totals.append(totals_map.get(cur, 0.0))
        cur = cur + relativedelta(months=1)

    # Current month total + budget
    this_month_start = date.today().replace(day=1)
    this_month_total = float(qs.filter(date__gte=this_month_start).aggregate(total=Sum('amount'))['total'] or 0)

    try:
        b = Budget.objects.get(user=user, month=this_month_start, category__isnull=True)
        monthly_budget_amount = float(b.amount)
    except Budget.DoesNotExist:
        monthly_budget_amount = None

    budget_percent = None
    budget_alert = False
    if monthly_budget_amount:
        budget_percent = (this_month_total / monthly_budget_amount) * 100
        if budget_percent >= 100:
            budget_alert = True

    recent_expenses = Expense.objects.filter(user=request.user).order_by('-date')[:10]


    context = {
        'overall_total': float(overall),
        'categories_json': json.dumps(categories),
        'category_amounts_json': json.dumps(category_amounts),
        'month_labels_json': json.dumps(month_labels),
        'month_totals_json': json.dumps(month_totals),
        'cat_qs': cat_qs,
        'monthly_qs': monthly_qs,
        'recent_expenses': recent_expenses,
        'this_month_total': this_month_total,
        'monthly_budget_amount': monthly_budget_amount,
        'budget_alert': budget_alert,
        'budget_percent': budget_percent,
        'total_categories': cat_qs.count(),
        'months_shown': len(month_labels),
        'username': request.user.username,
    }
    return render(request, 'expenses/dashboard.html', context)


# ------------------------
# CRUD Operations
# ------------------------
@login_required
def expense_list(request):
    qs = Expense.objects.filter(user=request.user).order_by('-date')

    q = request.GET.get('q')
    if q:
        qs = qs.filter(Q(description__icontains=q) | Q(category__name__icontains=q))

    start = request.GET.get('start')
    end = request.GET.get('end')
    if start:
        qs = qs.filter(date__gte=start)
    if end:
        qs = qs.filter(date__lte=end)

    # pagination
    from django.core.paginator import Paginator
    paginator = Paginator(qs, 20)
    page = request.GET.get('page') or 1
    expenses = paginator.get_page(page)

    return render(request, 'expenses/expense_list.html', {'expenses': expenses, 'q': q, 'start': start, 'end': end})


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.user = request.user
            exp.save()

            # Optional: Budget warning
            month_start = exp.date.replace(day=1)
            month_total = Expense.objects.filter(user=request.user, date__gte=month_start).aggregate(total=Sum('amount'))['total'] or 0
            try:
                b = Budget.objects.get(user=request.user, month=month_start, category__isnull=True)
                if month_total >= b.amount:
                    messages.warning(request, '⚠️ You have exceeded your monthly budget!')
            except Budget.DoesNotExist:
                pass

            messages.success(request, 'Expense added successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})


@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == "POST":
        # Read values manually from input fields
        expense.title = request.POST.get("title")
        expense.amount = request.POST.get("amount")
        expense.date = request.POST.get("date")
        expense.description = request.POST.get("description")

        # Category handling:
        category_name = request.POST.get("category")
        if category_name:
            category_obj, created = Category.objects.get_or_create(name=category_name)
            expense.category = category_obj

        expense.save()
        messages.success(request, "Expense updated successfully!")
        return redirect("expense_list")

    return render(request, "expenses/edit_expense.html", {"expense": expense})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, "Expense deleted successfully!")
        return redirect('expense_list')
    return render(request, 'expenses/delete_expense.html', {'expense': expense})


# ------------------------
# Extra Utilities
# ------------------------
@login_required
def month_total_api(request):
    start = date.today().replace(day=1)
    total = Expense.objects.filter(user=request.user, date__gte=start).aggregate(total=Sum('amount'))['total'] or 0
    return JsonResponse({'month_total': float(total)})


@login_required
def export_csv(request):
    qs = Expense.objects.filter(user=request.user).order_by('-date')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Category', 'Title', 'Description', 'Amount'])
    for e in qs:
        writer.writerow([
            e.date,
            e.category.name if e.category else '',
            e.title,
            e.description or '',
            float(e.amount)
        ])
    return response
