from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

class Command(BaseCommand):
    help = 'Create Floor Wing users for each floor in TECH and ARTS campuses.'

    def handle(self, *args, **options):
        # Define campuses and floors
        campuses = {
            'TECH': {
                'name': 'SNS College of Technology',
                'floors': [1, 2, 3, 4],
                'email_domain': 'floorwing.tech.com'
            },
            'ARTS': {
                'name': 'Dr. SNS Rajalakshmi College of Arts and Science',
                'floors': [1, 2, 3],
                'email_domain': 'floorwing.arts.com'
            }
        }
        default_password = 'FloorWing@123'
        for campus_key, campus_info in campuses.items():
            for floor in campus_info['floors']:
                email = f"floorwing{floor}@{campus_info['email_domain']}"
                username = f"floorwing_{campus_key.lower()}_{floor}"
                first_name = f"FloorWing{floor}"
                last_name = campus_key
                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=default_password,
                        first_name=first_name,
                        last_name=last_name
                    )
                    UserProfile.objects.filter(user=user).update(
                        role='FLOOR_WING',
                        campus=campus_key,
                        floor=floor
                    )
                    self.stdout.write(self.style.SUCCESS(f"Created {username} ({email}) for {campus_key} floor {floor}"))
                else:
                    self.stdout.write(self.style.WARNING(f"User {username} already exists."))
        self.stdout.write(self.style.SUCCESS('Floor Wing user creation complete.'))
