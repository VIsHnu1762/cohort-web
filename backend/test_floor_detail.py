#!/usr/bin/env python
"""
Test the admin floor detail endpoint
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from apps.profiles.models import UserProfile
from apps.profiles.admin_views import AdminFloorDetailView

# Create a request factory
factory = RequestFactory()

# Get admin user
admin_user = User.objects.get(username='testuser')
print(f"Testing as: {admin_user.username} (role: {admin_user.profile.role})")

# Test TECH Floor 1
print("\n=== Testing TECH Floor 1 ===")
request = factory.get('/api/profiles/admin/campus/TECH/floor/1/')
request.user = admin_user

view = AdminFloorDetailView.as_view()
try:
    response = view(request, campus='TECH', floor=1)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.data
        print(f"Students: {len(data.get('students', []))}")
        print(f"Mentors: {len(data.get('mentors', []))}")
        print(f"Floor Wing: {data.get('floor_wing')}")
        print(f"\nSample student:")
        if data.get('students'):
            print(f"  {data['students'][0]}")
    else:
        print(f"Error: {response.data}")
except Exception as e:
    print(f"Exception: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Testing ARTS Floor 2 ===")
request = factory.get('/api/profiles/admin/campus/ARTS/floor/2/')
request.user = admin_user

try:
    response = view(request, campus='ARTS', floor=2)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.data
        print(f"Students: {len(data.get('students', []))}")
        print(f"Mentors: {len(data.get('mentors', []))}")
        print(f"Floor Wing: {data.get('floor_wing')}")
except Exception as e:
    print(f"Exception: {e}")
    import traceback
    traceback.print_exc()
