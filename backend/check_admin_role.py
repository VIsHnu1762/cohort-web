import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

print("=" * 80)
print("CHECKING ALL USERS WITH admin@test.com EMAIL")
print("=" * 80)

users = User.objects.filter(email='admin@test.com')
print(f"\nFound {users.count()} user(s) with email 'admin@test.com'\n")

for user in users:
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Is Staff: {user.is_staff}")
    print(f"Is Superuser: {user.is_superuser}")
    
    try:
        profile = UserProfile.objects.get(user=user)
        print(f"Has Profile: True")
        print(f"Role: {profile.role}")
        print(f"Campus: {profile.campus}")
        print(f"Floor: {profile.floor}")
        
        if profile.role != 'ADMIN':
            print(f"\n⚠️  WARNING: Role is '{profile.role}', should be 'ADMIN'")
            print("Fixing role...")
            profile.role = 'ADMIN'
            profile.save()
            print("✓ Role updated to ADMIN")
    except UserProfile.DoesNotExist:
        print("Has Profile: False")
        print("ERROR: No UserProfile exists for this user!")
        print("\nCreating admin profile...")
        profile = UserProfile.objects.create(
            user=user,
            role='ADMIN',
            campus='TECH',
            floor=None
        )
        print("✓ Admin profile created successfully!")
        print(f"Role: {profile.role}")
    
    print("-" * 80)
