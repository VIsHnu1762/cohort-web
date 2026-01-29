"""
Import dummy users from CSV and create them as students on Floor 2, SNS College of Technology
"""
import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

def import_users():
    # Use campus and floor from UserProfile choices
    campus = 'TECH'  # SNS College of Technology
    floor = 2  # 2nd Year / Floor 2
    
    print(f"✅ Campus: SNS College of Technology")
    print(f"✅ Floor: 2nd Year")
    print("\n" + "="*60)
    
    # Read CSV file
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'dummy users - Sheet1.csv')
    
    created_count = 0
    updated_count = 0
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            email = row['email'].strip()
            username = row['username'].strip()
            password = 'pass123#'  # Using specified password
            
            # Create or update user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'first_name': username.split()[0] if username else '',
                    'last_name': ' '.join(username.split()[1:]) if len(username.split()) > 1 else ''
                }
            )
            
            if created:
                user.set_password(password)
                user.save()
                created_count += 1
                status = "✅ CREATED"
            else:
                # Update password for existing user
                user.set_password(password)
                user.save()
                updated_count += 1
                status = "🔄 UPDATED"
            
            # Create or update profile
            profile, profile_created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'role': 'STUDENT',
                    'campus': campus,
                    'floor': floor,
                }
            )
            
            if not profile_created:
                # Update existing profile
                profile.role = 'STUDENT'
                profile.campus = campus
                profile.floor = floor
                profile.save()
            
            print(f"{status} | {username:30} | {email:40} | Floor {floor}")
    
    print("\n" + "="*60)
    print(f"✅ Total Created: {created_count}")
    print(f"🔄 Total Updated: {updated_count}")
    print(f"📊 Total Processed: {created_count + updated_count}")
    print("\n🔑 All passwords set to: pass123#")
    print(f"🏢 Campus: SNS College of Technology")
    print(f"🏢 Floor: 2")
    print("="*60)

if __name__ == '__main__':
    import_users()
