import os
from django.core.wsgi import get_wsgi_application

settings_module = 'event_platform.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'event_platform.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
