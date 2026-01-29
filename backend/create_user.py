import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Create a new user
username = 'testuser'
email = 'test@example.com'
password = 'testpass123'

if User.objects.filter(username=username).exists():
    print(f"User '{username}' already exists!")
else:
    user = User.objects.create_user(username=username, email=email, password=password)
    print(f"User created successfully!")
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")
