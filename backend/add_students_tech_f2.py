import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

# Configuration
CAMPUS = 'TECH'
FLOOR = 2
DEFAULT_PASSWORD = 'student123'

# List of student names to add
STUDENTS = [
    'Ananya Reddy',
    'Karthik Murugan',
    'Priya Sundaram',
    'Aravind Kumar',
    'Deepika Rajan',
    # Add more student names here
]

def get_next_student_number():
    """Get the next available student number for TECH floor 2"""
    existing_students = UserProfile.objects.filter(
        campus='TECH',
        floor=2,
        role='STUDENT'
    )
    
    # Find the highest number from existing usernames
    max_num = 0
    for profile in existing_students:
        username = profile.user.username
        # Extract number from username like student_tech_f2_2CSE016
        if 'student_tech_f2_2CSE' in username:
            try:
                num = int(username.split('2CSE')[1])
                if num > max_num:
                    max_num = num
            except (ValueError, IndexError):
                continue
    
    return max_num + 1

def create_student(name, student_number):
    """Create a new student for TECH campus floor 2"""
    # Format: student_tech_f2_2CSE016
    username = f'student_tech_f2_2CSE{student_number:03d}'
    # Format: 2cse016@student.sns.edu
    email = f'2cse{student_number:03d}@student.sns.edu'
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f'❌ User {username} already exists')
        return None
    
    if User.objects.filter(email=email).exists():
        print(f'❌ Email {email} already in use')
        return None
    
    # Split name into first and last
    name_parts = name.split(' ', 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ''
    
    # Create user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=DEFAULT_PASSWORD,
        first_name=first_name,
        last_name=last_name,
        is_staff=False,
        is_superuser=False
    )
    
    # Create profile
    profile = UserProfile.objects.create(
        user=user,
        role='STUDENT',
        campus='TECH',
        floor=2
    )
    
    return user, profile

def main():
    print("=" * 80)
    print("ADDING NEW STUDENTS TO SNS COLLEGE OF TECHNOLOGY - FLOOR 2")
    print("=" * 80)
    print(f"Campus: SNS College of Technology (TECH)")
    print(f"Floor: 2")
    print(f"Default Password: {DEFAULT_PASSWORD}")
    print("=" * 80)
    
    if not STUDENTS:
        print("\n⚠️  No students to add. Edit the STUDENTS list in the script.")
        return
    
    # Get starting student number
    start_number = get_next_student_number()
    print(f"\nStarting from student number: 2CSE{start_number:03d}")
    print(f"Number of students to add: {len(STUDENTS)}\n")
    
    # Confirm before proceeding
    response = input("Proceed with adding students? (yes/no): ").strip().lower()
    if response != 'yes':
        print("Operation cancelled.")
        return
    
    # Create students
    created_count = 0
    for idx, name in enumerate(STUDENTS):
        student_number = start_number + idx
        result = create_student(name, student_number)
        
        if result:
            user, profile = result
            print(f"✓ Created: {user.username}")
            print(f"  Name: {name}")
            print(f"  Email: {user.email}")
            print(f"  Password: {DEFAULT_PASSWORD}")
            print(f"  Roll No: 2CSE{student_number:03d}")
            print("-" * 80)
            created_count += 1
    
    print(f"\n✓ Successfully created {created_count} out of {len(STUDENTS)} students")
    print("=" * 80)
    print("\nStudents can now login with:")
    print(f"  Email: <their_email>@student.sns.edu")
    print(f"  Password: {DEFAULT_PASSWORD}")
    print("=" * 80)

if __name__ == '__main__':
    main()
