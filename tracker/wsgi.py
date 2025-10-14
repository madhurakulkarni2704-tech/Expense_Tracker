import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'tracker' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tracker.settings')

# Create the WSGI application object for the server
application = get_wsgi_application()
