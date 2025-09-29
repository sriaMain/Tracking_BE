"""
WSGI config for Tracking_BE project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import django

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tracking_BE.settings')

# application = get_wsgi_application()
# django.setup()

# if os.environ.get("CREATE_SUPERUSER_ON_STARTUP", "True") == "True":
#     try:
#         from create_superuser import create_superadmin
#         create_superadmin()
#     except Exception as e:
#         print("Superuser creation failed:", e)

# import os
# from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tracking_BE.settings')

application = get_wsgi_application()

# Automatically create superuser on startup
if os.environ.get("CREATE_SUPERUSER_ON_STARTUP", "True") == "True":
    try:
        from create_superuser import create_superadmin
        create_superadmin()
    except Exception as e:
        print("Superuser creation failed:", e)
