import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

# Set a common password for all floor wing users
TEST_PASSWORD = 'floorwing123'

print("=" * 80)
print("SETTING PASSWORDS FOR ALL FLOOR WING USERS")
print("=" * 80)
print(f"New Password: {TEST_PASSWORD}")
print("=" * 80)

floor_wings = UserProfile.objects.filter(role='FLOOR_WING')
print(f"\nFound {floor_wings.count()} Floor Wing user(s)\n")

for profile in floor_wings:
    user = profile.user
    user.set_password(TEST_PASSWORD)
    user.save()
    
    print(f"✓ Username: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Name: {profile.user.first_name} {profile.user.last_name}".strip() or "N/A")
    print(f"  Campus: {profile.get_campus_display()}")
    print(f"  Floor: {profile.floor}")
    print(f"  Password: {TEST_PASSWORD}")
    print("-" * 80)

print(f"\n✓ All {floor_wings.count()} Floor Wing passwords have been set to: {TEST_PASSWORD}")
print("=" * 80)
