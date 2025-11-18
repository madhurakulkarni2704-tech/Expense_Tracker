from django.db import migrations

def create_default_categories(apps, schema_editor):
    Category = apps.get_model('expenses', 'Category')
    default_categories = [
        "Food",
        "Transport",
        "Shopping",
        "Bills",
        "Entertainment",
        "Other",
    ]

    for name in default_categories:
        Category.objects.get_or_create(name=name)

class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_profile_budget'),
    ]

    operations = [
        migrations.RunPython(create_default_categories),
    ]
