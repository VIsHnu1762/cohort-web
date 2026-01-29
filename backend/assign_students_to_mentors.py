"""
Script to assign students to mentors
Usage: python assign_students_to_mentors.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile


def assign_students_to_mentors():
    """Assign students evenly to available mentors"""
    
    # Get all mentors (staff users who are not superusers)
    mentors = User.objects.filter(is_staff=True, is_superuser=False).order_by('id')
    
    if not mentors.exists():
        print("❌ No mentors found! Please create staff users first.")
        return
    
    # Get all students (non-staff users)
    students = User.objects.filter(is_staff=False, is_superuser=False).order_by('id')
    
    if not students.exists():
        print("❌ No students found!")
        return
    
    print(f"📊 Found {mentors.count()} mentors and {students.count()} students")
    print(f"📌 Assigning ~{students.count() // mentors.count()} students per mentor\n")
    
    # Round-robin assignment
    mentor_list = list(mentors)
    mentor_assignments = {mentor: [] for mentor in mentor_list}
    
    for idx, student in enumerate(students):
        # Assign to mentor using round-robin
        mentor = mentor_list[idx % len(mentor_list)]
        
        # Update student's profile
        profile, created = UserProfile.objects.get_or_create(user=student)
        profile.assigned_mentor = mentor
        profile.save()
        
        mentor_assignments[mentor].append(student.username)
    
    # Print assignment summary
    print("✅ Assignment Complete!\n")
    for mentor, assigned_students in mentor_assignments.items():
        print(f"👤 {mentor.username} ({mentor.email})")
        print(f"   📝 Assigned {len(assigned_students)} students:")
        for student_username in assigned_students:
            print(f"      - {student_username}")
        print()
    
    print(f"💾 Total assignments: {students.count()} students assigned to {mentors.count()} mentors")


if __name__ == '__main__':
    assign_students_to_mentors()
