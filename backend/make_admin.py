#!/usr/bin/env python
"""
Make a user an admin
Usage: python make_admin.py <username_or_email>
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

if len(sys.argv) < 2:
    print("Usage: python make_admin.py <username_or_email>")
    print("\nAvailable users:")
    for user in User.objects.all()[:20]:
        role = user.profile.role if hasattr(user, 'profile') else 'No profile'
        print(f"  - {user.username} ({user.email}) - Current role: {role}")
    sys.exit(1)

identifier = sys.argv[1]

# Try to find user by username or email
try:
    user = User.objects.get(username=identifier)
except User.DoesNotExist:
    try:
        user = User.objects.get(email=identifier)
    except User.DoesNotExist:
        print(f"❌ User '{identifier}' not found")
        sys.exit(1)

# Get or create profile
if hasattr(user, 'profile'):
    profile = user.profile
else:
    profile = UserProfile.objects.create(user=user)

# Make admin
old_role = profile.role
profile.role = 'ADMIN'
profile.campus = None  # Admins don't belong to specific campus
profile.floor = None   # Admins don't belong to specific floor
profile.save()

# Also make superuser for Django admin access
if not user.is_superuser:
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f"✓ Also granted Django superuser access")

print(f"✅ SUCCESS!")
print(f"   User: {user.username} ({user.email})")
print(f"   Old role: {old_role}")
print(f"   New role: ADMIN")
print(f"\n   You can now login as admin at /admin/campus-select")
