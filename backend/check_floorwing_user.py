import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

email = 'fw_tech_f2@sns.edu'

print("=" * 80)
print(f"CHECKING USER: {email}")
print("=" * 80)

try:
    users = User.objects.filter(email=email)
    if users.count() == 0:
        print(f"❌ No user found with email: {email}")
        print("\nSearching for similar users...")
        similar = User.objects.filter(email__icontains='fw_tech')
        for u in similar:
            print(f"  - {u.username} ({u.email})")
    else:
        for user in users:
            print(f"\nUsername: {user.username}")
            print(f"Email: {user.email}")
            print(f"Is Active: {user.is_active}")
            print(f"Is Staff: {user.is_staff}")
            
            # Test password
            test_password = 'floorwing123'
            password_valid = user.check_password(test_password)
            print(f"Password Check ({test_password}): {password_valid}")
            
            if not password_valid:
                print(f"\n⚠️  Password incorrect! Setting to {test_password}...")
                user.set_password(test_password)
                user.save()
                print("✓ Password updated")
            
            try:
                profile = UserProfile.objects.get(user=user)
                print(f"Role: {profile.role}")
                print(f"Campus: {profile.get_campus_display()}")
                print(f"Floor: {profile.floor}")
            except UserProfile.DoesNotExist:
                print("❌ No UserProfile found!")
                
except Exception as e:
    print(f"Error: {e}")

print("=" * 80)
