"""
Create test users for E2E Selenium tests
This script creates all necessary test users with consistent credentials
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.profiles.models import UserProfile
from apps.gamification.models import Season, Episode, EpisodeProgress, SeasonScore
from datetime import date

User = get_user_model()

def create_or_update_user(username, email, password, role, is_staff=False, is_superuser=False):
    """Create or update a user with the given credentials"""
    try:
        user = User.objects.get(username=username)
        print(f"  Found existing user: {username}")
        # Update password and role
        user.set_password(password)
        user.role = role
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        print(f"  ✓ Updated {username} (role: {role})")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.role = role
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        print(f"  ✓ Created {username} (role: {role})")
    
    return user


def setup_student_profile(user):
    """Setup student profile with required data"""
    # Create UserProfile if doesn't exist
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'role': 'STUDENT',
            'campus': 'TECH',
            'floor': 2,
            'leetcode_id': f'{user.username}_leetcode',
            'github_id': f'{user.username}_github'
        }
    )
    if created:
        print(f"    Created profile for {user.username}")
    else:
        profile.role = 'STUDENT'
        profile.save()
    
    # Ensure there's an active season
    season = Season.objects.filter(is_active=True).first()
    if not season:
        season = Season.objects.create(
            name="Test Season 2025",
            season_number=1,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            is_active=True
        )
        print(f"    Created test season: {season.name}")
        
        # Create episodes for the season
        for ep_num in range(1, 5):
            Episode.objects.get_or_create(
                season=season,
                episode_number=ep_num,
                defaults={
                    'name': f'Episode {ep_num}',
                    'description': f'Test Episode {ep_num}'
                }
            )
    
    # Create EpisodeProgress for the first episode
    first_episode = Episode.objects.filter(season=season, episode_number=1).first()
    if first_episode:
        progress, created = EpisodeProgress.objects.get_or_create(
            student=user,
            episode=first_episode,
            defaults={
                'status': 'unlocked'
            }
        )
        if created:
            print(f"    Created episode progress for {user.username}")
    
    # Create SeasonScore if doesn't exist
    season_score, created = SeasonScore.objects.get_or_create(
        student=user,
        season=season,
        defaults={
            'total_score': 0
        }
    )
    if created:
        print(f"    Created season score for {user.username}")
    
    return profile


def setup_profile(user, role, campus='TECH', floor=2):
    """Setup user profile for any role"""
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'role': role,
            'campus': campus,
            'floor': floor
        }
    )
    if created:
        print(f"    Created {role} profile")
    else:
        profile.role = role
        profile.campus = campus
        profile.floor = floor
        profile.save()
        print(f"    Updated {role} profile")
    return profile


def main():
    print("=" * 60)
    print("Creating E2E Test Users")
    print("=" * 60)
    print()
    
    # Common password for all test users
    test_password = "test_password_123"
    
    # 1. Create test student
    print("1. Creating Test Student...")
    student_user = create_or_update_user(
        username="test_student",
        email="test_student@cohort.com",
        password=test_password,
        role="student"
    )
    setup_student_profile(student_user)
    print()
    
    # 2. Create test mentor
    print("2. Creating Test Mentor...")
    mentor_user = create_or_update_user(
        username="test_mentor",
        email="test_mentor@cohort.com",
        password=test_password,
        role="mentor",
        is_staff=True
    )
    setup_profile(mentor_user, 'MENTOR', campus='TECH', floor=2)
    print()
    
    # 3. Create test floor wing
    print("3. Creating Test Floor Wing...")
    floorwing_user = create_or_update_user(
        username="test_floorwing",
        email="test_floorwing@cohort.com",
        password=test_password,
        role="floor_wing",
        is_staff=True
    )
    setup_profile(floorwing_user, 'FLOOR_WING', campus='TECH', floor=2)
    print()
    
    # 4. Create test admin
    print("4. Creating Test Admin...")
    admin_user = create_or_update_user(
        username="test_admin",
        email="test_admin@cohort.com",
        password=test_password,
        role="admin",
        is_staff=True,
        is_superuser=False
    )
    setup_profile(admin_user, 'ADMIN', campus='TECH', floor=1)
    print()
    
    # 5. Create test superadmin (optional)
    print("5. Creating Test Super Admin...")
    superadmin_user = create_or_update_user(
        username="test_superadmin",
        email="test_superadmin@cohort.com",
        password=test_password,
        role="admin",
        is_staff=True,
        is_superuser=True
    )
    setup_profile(superadmin_user, 'ADMIN', campus='TECH', floor=1)
    print()
    
    print("=" * 60)
    print("✅ All E2E Test Users Created Successfully!")
    print("=" * 60)
    print()
    print("Test Credentials (All users have same password):")
    print(f"Password: {test_password}")
    print()
    print("Usernames:")
    print("  - test_student")
    print("  - test_mentor")
    print("  - test_floorwing")
    print("  - test_admin")
    print("  - test_superadmin")
    print()
    print("You can now run E2E tests with:")
    print("  pytest tests/e2e/ --base-url=http://localhost:5173 --api-url=http://localhost:8000")
    print()


if __name__ == "__main__":
    main()
