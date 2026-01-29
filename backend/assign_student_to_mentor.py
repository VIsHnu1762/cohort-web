"""
Assign testuser to mentor in database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

# Get or create mentor user
mentor, created = User.objects.get_or_create(
    username='mentor',
    defaults={
        'email': 'mentor@example.com',
        'is_staff': True,
        'is_superuser': False
    }
)
if created:
    mentor.set_password('mentor123')
    mentor.save()
    print(f"✅ Created mentor user")
else:
    print(f"✅ Mentor user exists: {mentor.username}")

# Get testuser
try:
    testuser = User.objects.get(username='testuser')
    print(f"✅ Found testuser: {testuser.username}")
except User.DoesNotExist:
    print("❌ testuser not found")
    exit(1)

# Get or create profiles
mentor_profile, _ = UserProfile.objects.get_or_create(user=mentor)
testuser_profile, _ = UserProfile.objects.get_or_create(user=testuser)

# Assign mentor to testuser
testuser_profile.assigned_mentor = mentor
testuser_profile.save()
print(f"✅ Assigned mentor {mentor.username} to student {testuser.username}")

# Verify - get all students assigned to this mentor
assigned_students = User.objects.filter(profile__assigned_mentor=mentor)
print(f"\nMentor {mentor.username} now has {assigned_students.count()} assigned students:")
for student in assigned_students:
    print(f"  - {student.username}")
