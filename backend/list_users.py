import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

print("\n" + "="*80)
print("USER LIST WITH CREDENTIALS")
print("="*80)

users = User.objects.all().select_related('profile')

print(f"\nTotal Users: {users.count()}\n")

# Group by role
roles = {
    'ADMIN': [],
    'FLOOR_WING': [],
    'MENTOR': [],
    'STUDENT': []
}

for user in users:
    try:
        profile = user.profile
        role = profile.role
        roles[role].append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': f"{user.first_name} {user.last_name}",
            'campus': profile.campus or 'N/A',
            'floor': profile.floor or 'N/A',
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
        })
    except:
        # User without profile
        print(f"⚠️  {user.username} - No profile")

# Print by role
for role, users_list in roles.items():
    if users_list:
        print(f"\n{'='*80}")
        print(f"{role}S ({len(users_list)})")
        print('='*80)
        for u in users_list:
            superuser = " [SUPERUSER]" if u['is_superuser'] else ""
            staff = " [STAFF]" if u['is_staff'] else ""
            print(f"\nUsername: {u['username']}{superuser}{staff}")
            print(f"Email:    {u['email']}")
            print(f"Name:     {u['name']}")
            print(f"Campus:   {u['campus']}")
            print(f"Floor:    {u['floor']}")
            print(f"ID:       {u['id']}")

print("\n" + "="*80)
print("PASSWORD INFORMATION")
print("="*80)
print("\n⚠️  SECURITY NOTE: User passwords are hashed in the database.")
print("⚠️  Django uses PBKDF2 algorithm - passwords cannot be reversed.")
print("\nIf you need to set a known password for testing:")
print("  python manage.py changepassword <username>")
print("\nOr use the Django shell:")
print("  python manage.py shell")
print("  >>> from django.contrib.auth.models import User")
print("  >>> user = User.objects.get(username='testuser')")
print("  >>> user.set_password('newpassword123')")
print("  >>> user.save()")

print("\n" + "="*80)
print("COMMON TEST PASSWORDS (if set during development)")
print("="*80)
print("\nThese are commonly used test passwords:")
print("  testpass123")
print("  password123")
print("  admin123")
print("  Test@123")

print("\n" + "="*80)
print("\nTo create a new user with known password:")
print("  python manage.py createsuperuser")
print("  Or run: python create_test_user.py")
print("="*80 + "\n")
