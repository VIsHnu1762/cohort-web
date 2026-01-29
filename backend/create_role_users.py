"""
Script to create test users for each role in the system.
Run: python manage.py shell < create_role_users.py
Or: python create_role_users.py (after setting up Django)
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

def create_users():
    """Create users for each role"""
    
    users_data = [
        {
            'username': 'admin',
            'email': 'admin@cohort.edu',
            'password': 'admin123',
            'role': 'ADMIN',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
        },
        {
            'username': 'mentor1',
            'email': 'mentor@cohort.edu',
            'password': 'mentor123',
            'role': 'MENTOR',
            'first_name': 'Test',
            'last_name': 'Mentor',
            'campus': 'TECH',
        },
        {
            'username': 'student1',
            'email': 'student@cohort.edu',
            'password': 'student123',
            'role': 'STUDENT',
            'first_name': 'Test',
            'last_name': 'Student',
            'campus': 'TECH',
            'floor': 2,
        },
        {
            'username': 'floorwing1',
            'email': 'floorwing@cohort.edu',
            'password': 'floorwing123',
            'role': 'FLOOR_WING',
            'first_name': 'Floor',
            'last_name': 'Wing',
            'campus': 'TECH',
            'floor': 1,
        },
    ]
    
    created_users = []
    
    for user_data in users_data:
        username = user_data['username']
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            print(f"⚠️  User '{username}' already exists, skipping...")
            continue
        
        # Extract profile fields
        role = user_data.pop('role')
        campus = user_data.pop('campus', None)
        floor = user_data.pop('floor', None)
        password = user_data.pop('password')
        
        # Create user
        user = User.objects.create_user(**user_data)
        user.set_password(password)
        user.save()
        
        # Update profile
        profile = user.profile
        profile.role = role
        if campus:
            profile.campus = campus
        if floor:
            profile.floor = floor
        profile.save()
        
        created_users.append({
            'username': username,
            'password': password,
            'role': role,
            'email': user.email
        })
        
        print(f"✅ Created {role}: {username} ({user.email})")
    
    # Print summary
    print("\n" + "="*60)
    print("USER CREDENTIALS SUMMARY")
    print("="*60)
    for user in created_users:
        print(f"\n{user['role']}:")
        print(f"  Username: {user['username']}")
        print(f"  Email:    {user['email']}")
        print(f"  Password: {user['password']}")
    print("\n" + "="*60)
    print("⚠️  IMPORTANT: Change these passwords after first login!")
    print("="*60)

if __name__ == '__main__':
    print("Creating users for each role...\n")
    create_users()
    print("\n✅ Done!")
