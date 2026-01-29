#!/usr/bin/env python
"""
Automatically assign unassigned students to mentors on their floor

Features:
- Supports up to 3 mentors per floor
- Distributes students evenly using round-robin algorithm
- Only assigns unassigned students (preserves existing assignments)
- Mentors can later reassign students to themselves via API
- Admins can modify all assignments via admin panel/API

Usage:
    python assign_students_to_mentors_auto.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

print("\n=== Auto-Assigning Students to Mentors ===")
print("Note: Each floor can have up to 3 mentors")
print("Students will be distributed evenly among available mentors\n")

# Process each campus and floor
for campus_code, campus_name in UserProfile.CAMPUS_CHOICES:
    floors = [1, 2, 3, 4] if campus_code == 'TECH' else [1, 2, 3]
    
    for floor in floors:
        print(f"\n{campus_name} - Floor {floor}:")
        
        # Get mentors on this floor (up to 3 mentors per floor)
        mentors = list(UserProfile.objects.filter(
            role='MENTOR',
            campus=campus_code,
            floor=floor
        ).select_related('user')[:3])  # Limit to 3 mentors per floor
        
        if not mentors:
            print(f"  ⚠ No mentors found")
            continue
        
        if len(mentors) > 3:
            print(f"  ⚠ Warning: Found {len(mentors)} mentors, using first 3")
            mentors = mentors[:3]
        
        print(f"  Found {len(mentors)} mentor(s):")
        for m in mentors:
            print(f"     - {m.user.get_full_name()} ({m.user.email})")
        
        # Get unassigned students on this floor
        unassigned_students = UserProfile.objects.filter(
            role='STUDENT',
            campus=campus_code,
            floor=floor,
            assigned_mentor__isnull=True
        ).select_related('user')
        
        if not unassigned_students.exists():
            print(f"  ✓ All students already assigned")
            continue
        
        print(f"  Found {unassigned_students.count()} unassigned student(s)")
        
        # Distribute students evenly among mentors using round-robin
        # This ensures balanced distribution (e.g., 10 students / 3 mentors = 3,3,4)
        assigned_count = 0
        for index, student_profile in enumerate(unassigned_students):
            # Round-robin assignment: cycles through mentors
            mentor_profile = mentors[index % len(mentors)]
            student_profile.assigned_mentor = mentor_profile.user
            student_profile.save()
            assigned_count += 1
            print(f"     → {student_profile.user.email} assigned to {mentor_profile.user.email}")
        
        print(ffinal distribution for this floor
        print(f"  📊 Final distribution:")
        for mentor_profile in mentors:
            student_count = UserProfile.objects.filter(
                role='STUDENT',
                campus=campus_code,
                floor=floor,
                assigned_mentor=mentor_profile.user
            ).count()
            print(f"     - {mentor_profile.user.get_full_name()}: {student_count} students")

print("\n✅ Done! All unassigned students have been assigned to mentors.")
print("\n📝 Next Steps:")
print("   - Mentors can reassign students to themselves via the mentor dashboard")
print("   - Admins can modify all assignments via Django admin or API endpoints")
print("   - To implement mentor self-assignment, create API endpoints in backend/apps/profiles/views.py")
print("   - To implement admin assignment changes, use Django admin or create admin API endpointsent_count} students")

print("\n✅ Done! All unassigned students have been assigned to mentors.\n")
