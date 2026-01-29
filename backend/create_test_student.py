"""
Create a test student user for gamification testing
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.profiles.models import UserProfile

User = get_user_model()

# Create test student
email = 'student@test.com'
username = 'student'
password = 'test123'

# Check if user exists
if User.objects.filter(email=email).exists():
    print(f'✓ User {email} already exists')
    user = User.objects.get(email=email)
else:
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name='Test',
        last_name='Student'
    )
    print(f'✓ Created user: {email}')

# Create or update profile
profile, created = UserProfile.objects.get_or_create(
    user=user,
    defaults={
        'phone': '1234567890',
        'roll_number': 'TEST001',
        'campus': 'Main Campus',
        'floor': '1',
        'wing': 'A',
    }
)

if created:
    print(f'✓ Created profile for {email}')
else:
    print(f'✓ Profile already exists for {email}')

print('\n' + '='*60)
print('TEST STUDENT CREATED SUCCESSFULLY!')
print('='*60)
print(f'Email: {email}')
print(f'Username: {username}')
print(f'Password: {password}')
print('='*60)
print('\nYou can now login with these credentials.')
