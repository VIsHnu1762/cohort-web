#!/usr/bin/env python
"""
Setup Floor Wing Users for Railway PostgreSQL Database
Creates floor wing users with proper campus and floor assignments
Run this on Railway: railway run python backend/setup_floorwings_railway.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

print("=" * 80)
print("RAILWAY DEPLOYMENT - FLOOR WING SETUP")
print("=" * 80)
print()

# Floor Wing configuration
FLOORWINGS = [
    # TECH campus - 4 floors
    {"username": "floorwing_tech_1", "email": "fw_tech_1@sns.edu", "campus": "TECH", "floor": 1, "name": "Floor Wing TECH Floor 1"},
    {"username": "floorwing_tech_2", "email": "fw_tech_2@sns.edu", "campus": "TECH", "floor": 2, "name": "Floor Wing TECH Floor 2"},
    {"username": "floorwing_tech_3", "email": "fw_tech_3@sns.edu", "campus": "TECH", "floor": 3, "name": "Floor Wing TECH Floor 3"},
    {"username": "floorwing_tech_4", "email": "fw_tech_4@sns.edu", "campus": "TECH", "floor": 4, "name": "Floor Wing TECH Floor 4"},
    
    # ARTS campus - 3 floors
    {"username": "floorwing_arts_1", "email": "fw_arts_1@sns.edu", "campus": "ARTS", "floor": 1, "name": "Floor Wing ARTS Floor 1"},
    {"username": "floorwing_arts_2", "email": "fw_arts_2@sns.edu", "campus": "ARTS", "floor": 2, "name": "Floor Wing ARTS Floor 2"},
    {"username": "floorwing_arts_3", "email": "fw_arts_3@sns.edu", "campus": "ARTS", "floor": 3, "name": "Floor Wing ARTS Floor 3"},
]

# Default password for all floor wings
DEFAULT_PASSWORD = 'floorwing123'

print(f"Creating {len(FLOORWINGS)} Floor Wing users...")
print(f"Default Password: {DEFAULT_PASSWORD}")
print()

created_count = 0
updated_count = 0
errors = []

for fw_data in FLOORWINGS:
    try:
        # Get or create user
        user, user_created = User.objects.get_or_create(
            username=fw_data['username'],
            defaults={
                'email': fw_data['email'],
                'first_name': fw_data['name'],
                'last_name': '',
            }
        )
        
        # Set password
        user.set_password(DEFAULT_PASSWORD)
        
        # Update email if needed
        if user.email != fw_data['email']:
            user.email = fw_data['email']
        
        user.save()
        
        # Get or create profile
        profile, profile_created = UserProfile.objects.get_or_create(user=user)
        
        # Set floor wing details
        profile.role = 'FLOOR_WING'
        profile.campus = fw_data['campus']
        profile.floor = fw_data['floor']
        profile.save()
        
        if user_created:
            created_count += 1
            status = "✅ CREATED"
        else:
            updated_count += 1
            status = "🔄 UPDATED"
            
        print(f"{status} {fw_data['username']}")
        print(f"   Email: {fw_data['email']}")
        print(f"   Campus: {fw_data['campus']}, Floor: {fw_data['floor']}")
        print(f"   Password: {DEFAULT_PASSWORD}")
        print()
        
    except Exception as e:
        error_msg = f"❌ ERROR creating {fw_data['username']}: {str(e)}"
        errors.append(error_msg)
        print(error_msg)
        print()

print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"✅ Created: {created_count}")
print(f"🔄 Updated: {updated_count}")
print(f"❌ Errors: {len(errors)}")
print()

if errors:
    print("ERRORS:")
    for error in errors:
        print(f"  {error}")
    print()

print("=" * 80)
print("VERIFICATION - All Floor Wing Users:")
print("=" * 80)

all_floor_wings = UserProfile.objects.filter(role='FLOOR_WING').select_related('user').order_by('campus', 'floor')

for profile in all_floor_wings:
    print(f"👤 {profile.user.username}")
    print(f"   Email: {profile.user.email}")
    print(f"   Campus: {profile.get_campus_display()}, Floor: {profile.floor}")
    print(f"   Login URL: https://your-frontend.up.railway.app")
    print()

print(f"Total Floor Wings in database: {all_floor_wings.count()}")
print("=" * 80)
print()
print("✅ Floor Wing setup complete!")
print()
print("NEXT STEPS:")
print("1. Test login with any floor wing user:")
print(f"   Username: floorwing_tech_1")
print(f"   Password: {DEFAULT_PASSWORD}")
print()
print("2. Floor wings can access their dashboard at:")
print("   https://your-frontend.up.railway.app/floor-wing-dashboard")
print()
print("=" * 80)
