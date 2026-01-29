import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

# Configuration
CAMPUS = 'TECH'
FLOOR = 2

def main():
    print("=" * 80)
    print("DELETING ALL STUDENTS FROM SNS COLLEGE OF TECHNOLOGY - FLOOR 2")
    print("=" * 80)
    
    # Get all students for TECH floor 2
    students = UserProfile.objects.filter(
        campus=CAMPUS,
        floor=FLOOR,
        role='STUDENT'
    ).select_related('user')
    
    count = students.count()
    
    if count == 0:
        print("\n✓ No students found in TECH Floor 2. Nothing to delete.")
        return
    
    print(f"\nFound {count} student(s) in TECH Floor 2:")
    print("-" * 80)
    for profile in students[:10]:  # Show first 10
        user = profile.user
        print(f"  - {user.username} ({user.first_name} {user.last_name}) - {user.email}")
    
    if count > 10:
        print(f"  ... and {count - 10} more")
    
    print("-" * 80)
    print("\n⚠️  WARNING: This will permanently delete these users!")
    print("⚠️  This action cannot be undone!")
    
    response = input(f"\nType 'DELETE ALL' to confirm deletion of {count} students: ").strip()
    
    if response != 'DELETE ALL':
        print("\nOperation cancelled. No students were deleted.")
        return
    
    # Delete all students
    deleted_count = 0
    for profile in students:
        user = profile.user
        username = user.username
        user.delete()  # This will cascade delete the profile
        print(f"✓ Deleted: {username}")
        deleted_count += 1
    
    print("\n" + "=" * 80)
    print(f"✓ Successfully deleted {deleted_count} students from TECH Floor 2")
    print("=" * 80)

if __name__ == '__main__':
    main()
