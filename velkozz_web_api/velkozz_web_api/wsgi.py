import os
import sys

from django.core.wsgi import get_wsgi_application
from django.conf import settings

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'velkozz_web_api.settings')
sys.path.append(os.path.join(settings.BASE_DIR, "apps"))

application = get_wsgi_application()
