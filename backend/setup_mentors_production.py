"""
Setup mentors and assign students in production database
Run: railway run python setup_mentors_production.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

def setup_mentors():
    """Create mentors and assign students"""
    
    print("\n" + "="*60)
    print("SETTING UP MENTORS IN PRODUCTION")
    print("="*60 + "\n")
    
    # Create Mentor 1
    print("1️⃣ Creating Mentor 1...")
    mentor1_email = 'mentor1@sns.edu'
    try:
        mentor1 = User.objects.get(email=mentor1_email)
        print(f"   ✓ Mentor 1 already exists: {mentor1_email}")
    except User.DoesNotExist:
        mentor1 = User.objects.create_user(
            username='mentor1_tech',
            email=mentor1_email,
            first_name='Rajesh',
            last_name='Kumar'
        )
        mentor1.set_password('mentor123')
        mentor1.save()
        print(f"   ✅ Created: {mentor1_email}")
    
    # Set Mentor 1 profile
    profile1 = mentor1.profile
    profile1.role = 'MENTOR'
    profile1.campus = 'TECH'
    profile1.floor = 1
    profile1.save()
    print(f"   ✓ Set role: MENTOR | Campus: TECH | Floor: 1")
    
    # Create Mentor 2
    print("\n2️⃣ Creating Mentor 2...")
    mentor2_email = 'mentor2@sns.edu'
    try:
        mentor2 = User.objects.get(email=mentor2_email)
        print(f"   ✓ Mentor 2 already exists: {mentor2_email}")
    except User.DoesNotExist:
        mentor2 = User.objects.create_user(
            username='mentor2_tech',
            email=mentor2_email,
            first_name='Priya',
            last_name='Sharma'
        )
        mentor2.set_password('mentor123')
        mentor2.save()
        print(f"   ✅ Created: {mentor2_email}")
    
    # Set Mentor 2 profile
    profile2 = mentor2.profile
    profile2.role = 'MENTOR'
    profile2.campus = 'TECH'
    profile2.floor = 2
    profile2.save()
    print(f"   ✓ Set role: MENTOR | Campus: TECH | Floor: 2")
    
    # Get all students (first 10)
    print("\n3️⃣ Getting students...")
    students = UserProfile.objects.filter(role='STUDENT').select_related('user')[:10]
    
    if students.count() < 10:
        print(f"   ⚠️  Only {students.count()} students found. Need at least 10 students.")
        print(f"   📝 Available students:")
        for student in students:
            print(f"      - {student.user.email}")
        return
    
    print(f"   ✓ Found {students.count()} students")
    
    # Assign first 5 students to Mentor 1
    print(f"\n4️⃣ Assigning students to Mentor 1 ({mentor1.email})...")
    for i, student_profile in enumerate(list(students)[:5]):
        student_profile.mentor = mentor1
        student_profile.save()
        print(f"   ✅ {i+1}. {student_profile.user.email} → Mentor 1")
    
    # Assign next 5 students to Mentor 2
    print(f"\n5️⃣ Assigning students to Mentor 2 ({mentor2.email})...")
    for i, student_profile in enumerate(list(students)[5:10]):
        student_profile.mentor = mentor2
        student_profile.save()
        print(f"   ✅ {i+1}. {student_profile.user.email} → Mentor 2")
    
    # Print summary
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE!")
    print("="*60)
    print("\n📊 SUMMARY:")
    print(f"   • Mentor 1: {mentor1.email} (ID: {mentor1.id})")
    print(f"     - {UserProfile.objects.filter(mentor=mentor1).count()} students assigned")
    print(f"   • Mentor 2: {mentor2.email} (ID: {mentor2.id})")
    print(f"     - {UserProfile.objects.filter(mentor=mentor2).count()} students assigned")
    
    print("\n🔑 MENTOR CREDENTIALS:")
    print(f"   Mentor 1: {mentor1_email} / mentor123")
    print(f"   Mentor 2: {mentor2_email} / mentor123")
    print("="*60 + "\n")
    
    # Print detailed assignments
    print("📋 DETAILED ASSIGNMENTS:")
    print(f"\nMentor 1 ({mentor1.email}) students:")
    for student in UserProfile.objects.filter(mentor=mentor1).select_related('user'):
        print(f"   - {student.user.email} ({student.user.first_name} {student.user.last_name})")
    
    print(f"\nMentor 2 ({mentor2.email}) students:")
    for student in UserProfile.objects.filter(mentor=mentor2).select_related('user'):
        print(f"   - {student.user.email} ({student.user.first_name} {student.user.last_name})")
    print()

if __name__ == '__main__':
    setup_mentors()
