"""
WSGI config for radeclaRest project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys


from django.core.wsgi import get_wsgi_application


# adjust the Python version in the line below as needed


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'radeclaRest.settings')

application = get_wsgi_application()
