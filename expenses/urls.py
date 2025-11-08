from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('add/', views.add_expense, name='add_expense'),
    path('edit/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),

     # Dashboard and analytics
    path('dashboard/', views.dashboard, name='dashboard'),         # main dashboard with graphs
    path('api/month_total/', views.month_total_api, name='month_total_api'),  # AJAX API for month total
    path('export/csv/', views.export_csv, name='export_csv'),   
    path('register/', views.register_view, name='register'),#8 nov 2025
    # CSV export
]
