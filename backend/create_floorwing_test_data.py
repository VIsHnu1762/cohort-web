#!/usr/bin/env python
"""
Create Test Data for Floor Wing Dashboard Testing
Creates floor wings, mentors, and students with proper assignments
"""
import os
import sys
import django
from django.db import transaction

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Group
from apps.profiles.models import UserProfile

# Test data configuration
CAMPUSES = {
    'TECH': {
        'name': 'SNS College of Technology',
        'floors': [1, 2, 3, 4],
        'floor_names': ['1st Year', '2nd Year', '3rd Year', '4th Year']
    },
    'ARTS': {
        'name': 'SNS College of Arts & Science',
        'floors': [1, 2, 3],
        'floor_names': ['1st Year', '2nd Year', '3rd Year']
    }
}

MENTORS_PER_FLOOR = 3
STUDENTS_PER_MENTOR = 5

# Sample names for realistic data
FIRST_NAMES = [
    'Arun', 'Priya', 'Karthik', 'Divya', 'Raj', 'Sneha', 'Vijay', 'Meena',
    'Kumar', 'Lakshmi', 'Suresh', 'Deepa', 'Mahesh', 'Kavya', 'Ramesh', 'Anjali',
    'Prakash', 'Nisha', 'Balaji', 'Sangeetha', 'Venkat', 'Revathi', 'Ganesh', 'Pooja',
    'Naveen', 'Shruthi', 'Mohan', 'Bhavani', 'Siva', 'Harini', 'Arjun', 'Sowmya',
    'Dinesh', 'Keerthana', 'Rajesh', 'Mythili', 'Kiran', 'Varsha', 'Prasad', 'Nandhini',
    'Anand', 'Pavithra', 'Bharath', 'Lavanya', 'Senthil', 'Radhika', 'Saravanan', 'Preethi'
]

LAST_NAMES = [
    'Kumar', 'Raj', 'Krishnan', 'Murugan', 'Selvam', 'Pandian', 'Rajan', 'Sundaram',
    'Natarajan', 'Ramesh', 'Shankar', 'Prakash', 'Anand', 'Babu', 'Gopal', 'Srinivasan'
]

def get_or_create_group(name):
    """Get or create a user group"""
    group, created = Group.objects.get_or_create(name=name)
    return group

def clear_existing_test_data():
    """Clear existing test data (optional)"""
    print("\n🗑️  Clearing existing test data...")
    
    # Delete test users (keep superuser)
    test_users = User.objects.filter(
        username__startswith='fw_'
    ) | User.objects.filter(
        username__startswith='mentor_'
    ) | User.objects.filter(
        username__startswith='student_'
    )
    
    count = test_users.count()
    test_users.delete()
    print(f"   ✅ Deleted {count} existing test users")

def create_floor_wing(campus_code, floor, index):
    """Create a floor wing user"""
    campus_info = CAMPUSES[campus_code]
    floor_name = campus_info['floor_names'][floor - 1]
    
    username = f'fw_{campus_code.lower()}_{floor}'
    email = f'{username}@sns.edu'
    
    # Create user
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': 'Floor Wing',
            'last_name': f'{campus_code} {floor_name}',
        }
    )
    
    if created:
        user.set_password('floorwing123')
        user.save()
    
    # Set profile
    profile = user.profile
    profile.role = 'FLOOR_WING'
    profile.campus = campus_code
    profile.floor = floor
    profile.save()
    
    # Add to group
    floorwing_group = get_or_create_group('floorwing')
    user.groups.add(floorwing_group)
    
    return user

def create_mentor(campus_code, floor, mentor_number):
    """Create a mentor user"""
    # Special names for SNS College of Technology 2nd Floor
    if campus_code == 'TECH' and floor == 2:
        mentor_names = {
            1: ('Reshma', 'Raj'),
            2: ('Gopi', 'Krishnan'),
            3: ('Tulsi', 'Krishna')
        }
        first_name, last_name = mentor_names.get(mentor_number, ('Mentor', f'F{floor}M{mentor_number}'))
    else:
        name_index = (floor - 1) * MENTORS_PER_FLOOR + mentor_number
        first_name = FIRST_NAMES[name_index % len(FIRST_NAMES)]
        last_name = LAST_NAMES[name_index % len(LAST_NAMES)]
    
    username = f'mentor_{campus_code.lower()}_f{floor}_m{mentor_number}'
    email = f'{username}@sns.edu'
    
    # Create user
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
        }
    )
    
    if created:
        user.set_password('mentor123')
        user.save()
    
    # Set profile
    profile = user.profile
    profile.role = 'MENTOR'
    profile.campus = campus_code
    profile.floor = floor
    profile.save()
    
    # Add to group
    mentor_group = get_or_create_group('mentor')
    user.groups.add(mentor_group)
    
    return user

def create_student(campus_code, floor, mentor_user, student_number):
    """Create a student user and assign to mentor"""
    # Calculate unique index for name selection
    base_index = (ord(campus_code[0]) * 100) + (floor * 20) + student_number
    first_name = FIRST_NAMES[base_index % len(FIRST_NAMES)]
    last_name = LAST_NAMES[(base_index + 5) % len(LAST_NAMES)]
    
    # Generate roll number
    year = floor
    dept_code = 'CSE' if campus_code == 'TECH' else 'BCA'
    roll_no = f'{year}{dept_code}{student_number:03d}'
    
    username = f'student_{campus_code.lower()}_f{floor}_{roll_no}'
    email = f'{roll_no.lower()}@student.sns.edu'
    
    # Create user
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
        }
    )
    
    if created:
        user.set_password('student123')
        user.save()
    
    # Set profile
    profile = user.profile
    profile.role = 'STUDENT'
    profile.campus = campus_code
    profile.floor = floor
    profile.assigned_mentor = mentor_user
    
    # Add platform IDs (optional)
    profile.leetcode_id = f'{first_name.lower()}{last_name.lower()}'
    profile.github_id = f'{first_name.lower()}-{last_name.lower()}'
    profile.linkedin_id = f'{first_name.lower()}-{last_name.lower()}-{student_number}'
    
    profile.save()
    
    # Add to group
    student_group = get_or_create_group('student')
    user.groups.add(student_group)
    
    return user

@transaction.atomic
def create_test_data():
    """Create all test data"""
    print("\n" + "=" * 70)
    print("🚀 Creating Floor Wing Test Data")
    print("=" * 70)
    
    stats = {
        'floor_wings': 0,
        'mentors': 0,
        'students': 0
    }
    
    # Create data for each campus
    for campus_code, campus_info in CAMPUSES.items():
        print(f"\n📍 {campus_info['name']}")
        print("-" * 70)
        
        for floor_index, floor in enumerate(campus_info['floors']):
            floor_name = campus_info['floor_names'][floor_index]
            
            print(f"\n  🏢 Floor {floor} ({floor_name})")
            
            # Create floor wing
            floor_wing = create_floor_wing(campus_code, floor, floor_index)
            stats['floor_wings'] += 1
            print(f"     ✅ Floor Wing: {floor_wing.username} (Password: floorwing123)")
            
            # Create mentors for this floor
            print(f"     👨‍🏫 Creating {MENTORS_PER_FLOOR} mentors...")
            mentors = []
            
            for mentor_num in range(1, MENTORS_PER_FLOOR + 1):
                mentor = create_mentor(campus_code, floor, mentor_num)
                mentors.append(mentor)
                stats['mentors'] += 1
                print(f"        ✓ {mentor.get_full_name()} ({mentor.username})")
            
            # Create students for each mentor
            print(f"     👥 Creating {STUDENTS_PER_MENTOR} students per mentor...")
            
            for mentor_index, mentor in enumerate(mentors):
                base_student_num = (mentor_index * STUDENTS_PER_MENTOR) + 1
                
                for student_offset in range(STUDENTS_PER_MENTOR):
                    student_num = base_student_num + student_offset
                    student = create_student(campus_code, floor, mentor, student_num)
                    stats['students'] += 1
            
            print(f"        ✓ {len(mentors) * STUDENTS_PER_MENTOR} students assigned")
    
    # Print summary
    print("\n" + "=" * 70)
    print("📊 Creation Summary")
    print("=" * 70)
    print(f"✅ Floor Wings Created: {stats['floor_wings']}")
    print(f"✅ Mentors Created: {stats['mentors']}")
    print(f"✅ Students Created: {stats['students']}")
    print(f"✅ Total Users: {stats['floor_wings'] + stats['mentors'] + stats['students']}")
    
    # Print login information
    print("\n" + "=" * 70)
    print("🔐 Sample Login Credentials")
    print("=" * 70)
    
    print("\n📌 Floor Wings (Password: floorwing123)")
    print("   Tech Campus:")
    for floor in [1, 2, 3, 4]:
        username = f'fw_tech_{floor}'
        print(f"      • {username}@sns.edu")
    
    print("\n   Arts Campus:")
    for floor in [1, 2, 3]:
        username = f'fw_arts_{floor}'
        print(f"      • {username}@sns.edu")
    
    print("\n📌 Sample Mentor (Password: mentor123)")
    print(f"   • mentor_tech_f1_m1@sns.edu")
    
    print("\n📌 Sample Student (Password: student123)")
    print(f"   • 1cse001@student.sns.edu")
    
    print("\n" + "=" * 70)
    print("✨ Test Data Creation Complete!")
    print("=" * 70)
    print("\n💡 Tips:")
    print("   1. Login as a floor wing to test the dashboard")
    print("   2. Try assigning/reassigning students to different mentors")
    print("   3. Create announcements and test the flow")
    print("   4. Check real-time data updates across tabs")
    print("\n")

def main():
    """Main execution"""
    import sys
    
    # Ask for confirmation
    print("\n" + "=" * 70)
    print("⚠️  WARNING: This will create test users in the database")
    print("=" * 70)
    print(f"\nThis script will create:")
    print(f"  • 7 Floor Wing users (4 Tech + 3 Arts)")
    print(f"  • 21 Mentor users (3 per floor)")
    print(f"  • 105 Student users (5 per mentor)")
    print(f"  • Total: 133 users\n")
    
    response = input("Do you want to proceed? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        # Optional: Clear existing test data
        clear_response = input("\nClear existing test data first? (yes/no): ").strip().lower()
        if clear_response in ['yes', 'y']:
            clear_existing_test_data()
        
        # Create test data
        create_test_data()
        
        print("✅ Done! You can now login and test the Floor Wing dashboard.\n")
    else:
        print("\n❌ Cancelled. No data was created.\n")

if __name__ == '__main__':
    main()
