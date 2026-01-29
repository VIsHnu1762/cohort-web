#!/usr/bin/env python
"""
Reset passwords for Floor 2 mentors
Sets password to 'mentor123' for all three mentors
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

print("\n=== Resetting Mentor Passwords ===\n")

mentors = [
    'reshma@cohort.com',
    'gopikannan@cohort.com',
    'thulasi@cohort.com',
    'mentor1@cohort.com',
    'mentor2@cohort.com'
]

password = 'mentor123'
hashed_password = make_password(password)

print(f"New password hash: {hashed_password[:60]}...\n")

for email in mentors:
    try:
        user = User.objects.get(email=email)
        user.password = hashed_password
        user.save()
        print(f"✅ Reset password for: {user.email} ({user.get_full_name()})")
    except User.DoesNotExist:
        print(f"⚠️  User not found: {email}")

print(f"\n✅ Done! All mentors can now login with password: {password}")
print(f"🔐 Login as: reshma@cohort.com / {password}\n")
