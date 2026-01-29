import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

print("=== Making User a Mentor (Staff Member) ===\n")

username = input("Enter username to make mentor: ")

try:
    user = User.objects.get(username=username)
    print(f"\nUser found: {user.username}")
    print(f"Current status:")
    print(f"  - is_staff: {user.is_staff}")
    print(f"  - is_superuser: {user.is_superuser}")
    
    if not user.is_staff:
        user.is_staff = True
        user.save()
        print(f"\n✅ {username} is now a mentor (staff member)!")
    else:
        print(f"\n✅ {username} is already a mentor!")
        
except User.DoesNotExist:
    print(f"\n❌ User '{username}' not found!")
    print("\nAvailable users:")
    for u in User.objects.all():
        print(f"  - {u.username} (staff: {u.is_staff}, superuser: {u.is_superuser})")
