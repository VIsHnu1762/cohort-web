"""
Create mentor account for tech floor 2 module 3
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

# Create or update mentor user
email = 'mentor_tech_f2_m3@sns.edu'
username = 'mentor_tech_f2_m3'
password = 'mentor123'

try:
    user = User.objects.get(email=email)
    print(f"✓ User already exists: {email}")
except User.DoesNotExist:
    user = User.objects.create_user(
        username=username,
        email=email,
        first_name='Mentor',
        last_name='Tech F2 M3'
    )
    user.set_password(password)
    user.save()
    print(f"✓ Created user: {email}")

# Ensure profile exists with MENTOR role
try:
    profile = user.profile
    profile.role = 'MENTOR'
    profile.campus = 'TECH'
    profile.floor = 2
    profile.save()
    print(f"✓ Updated profile to MENTOR role")
except:
    profile = UserProfile.objects.create(
        user=user,
        role='MENTOR',
        campus='TECH',
        floor=2
    )
    print(f"✓ Created profile with MENTOR role")

print(f"\n{'='*60}")
print(f"Mentor Account Created Successfully!")
print(f"{'='*60}")
print(f"Email: {email}")
print(f"Username: {username}")
print(f"Password: {password}")
print(f"Role: {profile.role}")
print(f"Campus: {profile.campus}")
print(f"Floor: {profile.floor}")
print(f"{'='*60}")
