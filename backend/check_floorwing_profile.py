import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

# Check floor wing users
floor_wing_users = UserProfile.objects.filter(role='FLOOR_WING')

print("\n=== Floor Wing Users Profile Check ===\n")
for profile in floor_wing_users:
    print(f"Username: {profile.user.username}")
    print(f"  Role: {profile.role}")
    print(f"  Campus: {profile.campus if profile.campus else 'NOT SET'}")
    print(f"  Floor: {profile.floor if profile.floor else 'NOT SET'}")
    print(f"  Has profile: {hasattr(profile.user, 'profile')}")
    print()

# Check if there are any floor wing users without campus/floor
missing_data = floor_wing_users.filter(campus__isnull=True) | floor_wing_users.filter(floor__isnull=True)
if missing_data.exists():
    print("❌ ISSUE FOUND: Floor wing users without campus/floor:")
    for profile in missing_data:
        print(f"  - {profile.user.username} (campus={profile.campus}, floor={profile.floor})")
else:
    print("✅ All floor wing users have campus and floor set")
