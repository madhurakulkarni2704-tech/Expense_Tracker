from django.apps import AppConfig

class ExpensesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expenses'
#8 n0v 2025
    def ready(self):
        import expenses.signals  # this line makes Django load your signals