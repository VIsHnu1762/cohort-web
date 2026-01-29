"""
Test script to create a test user and verify CLT API integration
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Create test user
username = 'testuser'
email = 'test@example.com'
password = 'testpass123'

if User.objects.filter(username=username).exists():
    print(f"✓ User '{username}' already exists")
    user = User.objects.get(username=username)
else:
    user = User.objects.create_user(username=username, email=email, password=password)
    print(f"✓ Created user '{username}' with password '{password}'")

print(f"\nTest User Credentials:")
print(f"Username: {username}")
print(f"Password: {password}")
print(f"Email: {email}")
print(f"\nYou can now use these credentials to:")
print(f"1. Get JWT token: POST http://localhost:8000/api/auth/token/")
print(f"2. Test CLT API: Use token in Authorization: Bearer <token>")
