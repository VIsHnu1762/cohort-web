import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

student = User.objects.get(username='test_student')
mentor = student.profile.assigned_mentor

print(f'Student: {student.username} ({student.email})')
if mentor:
    print(f'Assigned Mentor: {mentor.username} ({mentor.email})')
else:
    print('Assigned Mentor: None')
