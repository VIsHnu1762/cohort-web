import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

print("=== Quick Floor Wing Setup ===\n")

# Floor Wing usernames and assignments
floorwings = [
    # TECH campus
    {"username": f"floorwing_tech_{i}", "campus": "TECH", "floor": i} for i in range(1, 5)
] + [
    # ARTS campus
    {"username": f"floorwing_arts_{i}", "campus": "ARTS", "floor": i} for i in range(1, 4)
]

print("Assigning the following users as Floor Wings:")
for fw in floorwings:
    try:
        user = User.objects.get(username=fw["username"])
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.role = "FLOOR_WING"
        profile.campus = fw["campus"]
        profile.floor = fw["floor"]
        profile.save()
        print(f"  ✅ {fw['username']} is now a Floor Wing for {fw['campus']} floor {fw['floor']}!")
    except User.DoesNotExist:
        print(f"  ⚠️ {fw['username']} not found")

print("\n=== Floor Wing Users ===")
for profile in UserProfile.objects.filter(role="FLOOR_WING"):
    print(f"  - {profile.user.username} ({profile.campus} floor {profile.floor})")
