import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

# Check one of the created students
email = 'nitya.b.it.2024@snsce.ac.in'

try:
    user = User.objects.get(email=email)
    print("=" * 80)
    print(f"USER DETAILS: {email}")
    print("=" * 80)
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Is Active: {user.is_active}")
    print(f"Is Staff: {user.is_staff}")
    print(f"Is Superuser: {user.is_superuser}")
    
    # Test password
    password_check = user.check_password('pass123#')
    print(f"Password Check (pass123#): {password_check}")
    
    # Check profile
    try:
        profile = UserProfile.objects.get(user=user)
        print(f"\nPROFILE:")
        print(f"Role: {profile.role}")
        print(f"Campus: {profile.campus}")
        print(f"Floor: {profile.floor}")
        print(f"Assigned Mentor: {profile.assigned_mentor}")
        
        if profile.role != 'STUDENT':
            print(f"\n⚠️  WARNING: Role is '{profile.role}', should be 'STUDENT'")
    except UserProfile.DoesNotExist:
        print("\n❌ ERROR: No UserProfile found!")
        
    print("=" * 80)
        
except User.DoesNotExist:
    print(f"❌ User not found: {email}")
