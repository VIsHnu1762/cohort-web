#!/usr/bin/env python
"""Simple script to import users - run with: python import_users_simple.py"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile
import csv

def main():
    print("="*60)
    print("RAILWAY DEPLOYMENT - USER IMPORT")
    print("="*60)
    print("\nStarting import...")
    
    # First, create admin if doesn't exist
    admin_email = "admin@test.com"
    if not User.objects.filter(email=admin_email).exists():
        admin = User.objects.create_superuser(
            username='admin',
            email=admin_email,
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        print(f"✅ Created admin user: {admin_email}")
        print(f"   Username: admin")
        print(f"   Password: admin123")
    else:
        # Update password in case it changed
        admin = User.objects.get(email=admin_email)
        admin.set_password('admin123')
        admin.save()
        print(f"✅ Admin user exists and password updated: {admin_email}")
    
    # Import CSV users - try multiple locations
    csv_paths = [
        os.path.join(os.path.dirname(__file__), 'dummy users - Sheet1.csv'),  # backend/
        os.path.join(os.path.dirname(__file__), '..', 'dummy users - Sheet1.csv'),  # project root
        '/app/dummy users - Sheet1.csv',  # Railway root
        '/app/backend/dummy users - Sheet1.csv',  # Railway backend
    ]
    
    csv_path = None
    for path in csv_paths:
        if os.path.exists(path):
            csv_path = path
            break
    
    if not csv_path:
        print(f"⚠️  CSV not found in any of these locations:")
        for path in csv_paths:
            print(f"   - {path}")
        print(f"   Skipping dummy user import")
        return
    
    campus = 'TECH'
    floor = 2
    created = 0
    updated = 0
    
    print(f"\nImporting students from CSV...")
    print(f"Campus: SNS College of Technology")
    print(f"Floor: 2nd Year")
    print("-"*60)
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row['email'].strip()
            username = row['username'].strip()
            
            user, is_new = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'first_name': username.split()[0] if username else '',
                    'last_name': ' '.join(username.split()[1:]) if len(username.split()) > 1 else ''
                }
            )
            
            user.set_password('pass123#')
            user.save()
            
            profile, _ = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'STUDENT', 'campus': campus, 'floor': floor}
            )
            profile.role = 'STUDENT'
            profile.campus = campus
            profile.floor = floor
            profile.save()
            
            if is_new:
                created += 1
            else:
                updated += 1
            
            print(f"{'✅ Created' if is_new else '🔄 Updated'}: {username[:30]:<30} | {email}")
    
    print("-"*60)
    print(f"\n✅ IMPORT COMPLETE!")
    print(f"   Admin created: 1")
    print(f"   Students created: {created}")
    print(f"   Students updated: {updated}")
    print(f"   Total students: {created + updated}")
    print("\n📋 LOGIN CREDENTIALS:")
    print(f"   Admin: admin@test.com / admin123")
    print(f"   Students: <email> / pass123#")
    print("="*60)

if __name__ == '__main__':
    main()
