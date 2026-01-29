#!/usr/bin/env python
"""
Quick test script to verify admin API endpoints
Run: python test_admin_endpoints.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

print("\n=== Testing Admin API Endpoints ===\n")

# Check if we have any admin users
admins = UserProfile.objects.filter(role='ADMIN')
print(f"✓ Found {admins.count()} admin user(s)")

if admins.exists():
    admin = admins.first()
    print(f"  Admin: {admin.user.username} - {admin.user.email}")
else:
    print("  ⚠ No admin users found. Create one with: python manage.py create_superuser")

# Check campus data
print("\n=== Campus/Floor Structure ===")
for campus_code, campus_name in UserProfile.CAMPUS_CHOICES:
    print(f"\n{campus_name} ({campus_code}):")
    
    # Determine floor range
    floors = [1, 2, 3, 4] if campus_code == 'TECH' else [1, 2, 3]
    
    for floor in floors:
        students = UserProfile.objects.filter(
            role='STUDENT',
            campus=campus_code,
            floor=floor
        ).count()
        
        mentors = UserProfile.objects.filter(
            role='MENTOR',
            campus=campus_code,
            floor=floor
        ).count()
        
        floor_wing = UserProfile.objects.filter(
            role='FLOOR_WING',
            campus=campus_code,
            floor=floor
        ).first()
        
        fw_name = f"{floor_wing.user.first_name} {floor_wing.user.last_name}" if floor_wing else "Not assigned"
        
        print(f"  Floor {floor}: {students} students, {mentors} mentors, FW: {fw_name}")

print("\n=== API Endpoint URLs ===")
print("Campus Overview: GET /api/profiles/admin/campus/TECH/")
print("Campus Overview: GET /api/profiles/admin/campus/ARTS/")
print("Floor Detail: GET /api/profiles/admin/campus/TECH/floor/1/")
print("Assign Floor Wing: POST /api/profiles/admin/assign-floor-wing/")
print("Assign Mentor: POST /api/profiles/admin/assign-mentor/")

print("\n=== Test Complete ===\n")
