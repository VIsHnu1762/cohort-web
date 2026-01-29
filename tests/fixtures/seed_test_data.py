"""
Test data fixtures and database seeders
"""
import os
import sys
import django

# Add Django backend to path
backend_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backend')
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.users.models import Student, Mentor, FloorWing
from apps.gamification.models import Season, Episode, Title

User = get_user_model()


class TestDataSeeder:
    """Seed test data for E2E tests"""
    
    @staticmethod
    def create_test_users():
        """Create test users for all roles"""
        users_data = [
            {
                "username": "test_student",
                "email": "student@test.com",
                "password": "test_password_123",
                "role": "student",
                "first_name": "Test",
                "last_name": "Student"
            },
            {
                "username": "test_student_2",
                "email": "student2@test.com",
                "password": "test_password_123",
                "role": "student",
                "first_name": "Student",
                "last_name": "Two"
            },
            {
                "username": "test_mentor",
                "email": "mentor@test.com",
                "password": "test_password_123",
                "role": "mentor",
                "first_name": "Test",
                "last_name": "Mentor"
            },
            {
                "username": "test_floorwing",
                "email": "floorwing@test.com",
                "password": "test_password_123",
                "role": "floor_wing",
                "first_name": "Test",
                "last_name": "FloorWing"
            },
            {
                "username": "test_admin",
                "email": "admin@test.com",
                "password": "test_password_123",
                "role": "admin",
                "first_name": "Test",
                "last_name": "Admin",
                "is_staff": True
            },
            {
                "username": "superadmin",
                "email": "superadmin@test.com",
                "password": "admin_password_123",
                "role": "admin",
                "first_name": "Super",
                "last_name": "Admin",
                "is_staff": True,
                "is_superuser": True
            }
        ]
        
        created_users = []
        
        for user_data in users_data:
            role = user_data.pop("role")
            username = user_data["username"]
            
            # Check if user exists
            if User.objects.filter(username=username).exists():
                print(f"⚠️  User {username} already exists, skipping...")
                user = User.objects.get(username=username)
            else:
                # Create user
                password = user_data.pop("password")
                is_staff = user_data.pop("is_staff", False)
                is_superuser = user_data.pop("is_superuser", False)
                
                user = User.objects.create_user(
                    **user_data,
                    is_staff=is_staff,
                    is_superuser=is_superuser
                )
                user.set_password(password)
                user.save()
                
                # Create role-specific profile
                if role == "student":
                    Student.objects.get_or_create(
                        user=user,
                        defaults={
                            "roll_number": f"TEST{user.id:04d}",
                            "batch": "2024"
                        }
                    )
                elif role == "mentor":
                    Mentor.objects.get_or_create(
                        user=user,
                        defaults={
                            "department": "Computer Science"
                        }
                    )
                elif role == "floor_wing":
                    FloorWing.objects.get_or_create(
                        user=user,
                        defaults={
                            "floor_number": 1,
                            "wing": "A"
                        }
                    )
                
                print(f"✅ Created {role}: {username}")
            
            created_users.append(user)
        
        return created_users
    
    @staticmethod
    def create_seasons_and_episodes():
        """Create test seasons and episodes"""
        # Create seasons
        seasons_data = [
            {
                "name": "Season 1",
                "season_number": 1,
                "start_date": "2024-01-01",
                "end_date": "2024-03-31",
                "is_active": False
            },
            {
                "name": "Season 2",
                "season_number": 2,
                "start_date": "2024-04-01",
                "end_date": "2024-06-30",
                "is_active": True
            }
        ]
        
        for season_data in seasons_data:
            Season.objects.get_or_create(
                season_number=season_data["season_number"],
                defaults=season_data
            )
            print(f"✅ Created {season_data['name']}")
        
        # Create episodes for Season 2
        season_2 = Season.objects.get(season_number=2)
        episodes_data = [
            {"episode_number": 1, "name": "Episode 1"},
            {"episode_number": 2, "name": "Episode 2"},
            {"episode_number": 3, "name": "Episode 3"},
            {"episode_number": 4, "name": "Episode 4"},
            {"episode_number": 5, "name": "Episode 5"},
        ]
        
        for ep_data in episodes_data:
            Episode.objects.get_or_create(
                season=season_2,
                episode_number=ep_data["episode_number"],
                defaults=ep_data
            )
            print(f"✅ Created {ep_data['name']}")
    
    @staticmethod
    def create_titles():
        """Create test titles for redemption"""
        titles_data = [
            {"name": "Code Warrior", "cost": 10, "rarity": "common"},
            {"name": "Bug Hunter", "cost": 20, "rarity": "rare"},
            {"name": "Algorithm Master", "cost": 50, "rarity": "epic"},
            {"name": "Legend", "cost": 100, "rarity": "legendary"},
        ]
        
        for title_data in titles_data:
            Title.objects.get_or_create(
                name=title_data["name"],
                defaults=title_data
            )
            print(f"✅ Created title: {title_data['name']}")
    
    @staticmethod
    def assign_student_to_mentor():
        """Assign test student to test mentor"""
        try:
            student = Student.objects.get(user__username="test_student")
            mentor = Mentor.objects.get(user__username="test_mentor")
            
            student.mentor = mentor
            student.save()
            print("✅ Assigned test_student to test_mentor")
        except Exception as e:
            print(f"⚠️  Failed to assign student to mentor: {e}")
    
    @staticmethod
    def cleanup_test_data():
        """Remove all test data"""
        # Delete test users
        test_usernames = [
            "test_student",
            "test_student_2",
            "test_mentor",
            "test_floorwing",
            "test_admin",
        ]
        
        for username in test_usernames:
            User.objects.filter(username=username).delete()
        
        print("✅ Cleaned up test data")
    
    @staticmethod
    def seed_all():
        """Seed all test data"""
        print("\n🌱 Seeding test data...\n")
        
        TestDataSeeder.create_test_users()
        TestDataSeeder.create_seasons_and_episodes()
        TestDataSeeder.create_titles()
        TestDataSeeder.assign_student_to_mentor()
        
        print("\n✅ Test data seeding complete!\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "cleanup":
        TestDataSeeder.cleanup_test_data()
    else:
        TestDataSeeder.seed_all()
