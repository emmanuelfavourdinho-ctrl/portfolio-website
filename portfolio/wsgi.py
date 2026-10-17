"""
WSGI config for portfolio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Debug: print the port Render assigned
port = os.environ.get("PORT", "not set")
print(f"🚀 Render is assigning PORT = {port}")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

application = get_wsgi_application()

import os
print("Render port:", os.environ.get("PORT"))
