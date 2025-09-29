import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Tracking_BE.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="Teerdaveni",
        email="teerdaveni@sriainfotech.com",
        password="Teerdaveni@2025"
    )
    print("Superuser created!")
else:
    print("Superuser already exists.")
