import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

# Test the student that was having issues
email = "nitya.b.it.2024@snsce.ac.in"

print("\n=== Student Login Verification ===\n")

try:
    user = User.objects.get(email=email)
    print(f"✅ User found: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Is Active: {user.is_active}")
    print(f"  Password Check (pass123#): {user.check_password('pass123#')}")
    
    if hasattr(user, 'profile'):
        profile = user.profile
        print(f"\n  Profile Details:")
        print(f"    Role: {profile.role}")
        print(f"    Campus: {profile.campus}")
        print(f"    Floor: {profile.floor}")
        print(f"    Mentor: {profile.assigned_mentor.username if profile.assigned_mentor else 'None'}")
        
        # Check if role is correct
        if profile.role == 'STUDENT':
            print("\n  ✅ User has STUDENT role - should be able to access student pages")
        else:
            print(f"\n  ❌ User has wrong role: {profile.role}")
    else:
        print("\n  ❌ User has no profile!")
        
except User.DoesNotExist:
    print(f"❌ User with email {email} not found")
except Exception as e:
    print(f"❌ Error: {e}")

# Also check a few other students
print("\n\n=== Sample Student Check ===\n")
students = UserProfile.objects.filter(role='STUDENT', campus='TECH', floor=2)[:5]
for profile in students:
    print(f"{profile.user.email} - Role: {profile.role} - Active: {profile.user.is_active}")
