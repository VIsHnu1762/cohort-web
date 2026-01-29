import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

print("=== Quick Mentor Setup ===\n")

# List of users who should be mentors
mentor_usernames = ['mentor1', 'mentor2', 'mentor3', 'mentor']

print("Making the following users mentors:")
for username in mentor_usernames:
    try:
        user = User.objects.get(username=username)
        if not user.is_staff:
            user.is_staff = True
            user.save()
            print(f"  ✅ {username} is now a mentor!")
        else:
            print(f"  ✓ {username} already a mentor")
    except User.DoesNotExist:
        print(f"  ⚠️ {username} not found")

print("\n=== Staff Users ===")
for user in User.objects.filter(is_staff=True):
    print(f"  - {user.username} (superuser: {user.is_superuser})")
