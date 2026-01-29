import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Test user credentials
users = [
    {'username': 'student', 'email': 'student@test.com', 'password': 'student123', 'role': 'student'},
    {'username': 'mentor', 'email': 'mentor@test.com', 'password': 'mentor123', 'role': 'mentor'},
    {'username': 'admin', 'email': 'admin@test.com', 'password': 'admin123', 'role': 'admin'},
]

print("Creating test users...\n")

for user_data in users:
    username = user_data['username']
    email = user_data['email']
    password = user_data['password']
    role = user_data['role']
    
    # Delete user if exists
    User.objects.filter(username=username).delete()
    User.objects.filter(email=email).delete()
    
    # Create user
    if role == 'admin':
        user = User.objects.create_superuser(username=username, email=email, password=password)
    elif role == 'mentor':
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = True  # Mentors need staff privileges
        user.save()
    else:
        user = User.objects.create_user(username=username, email=email, password=password)
    
    print(f"✓ Created {role}: {email} / {password}")

print("\n✅ All test users created successfully!")
print("\nLogin Credentials:")
print("=" * 50)
for user_data in users:
    print(f"Role: {user_data['role'].upper()}")
    print(f"  Email: {user_data['email']}")
    print(f"  Password: {user_data['password']}")
    print()
